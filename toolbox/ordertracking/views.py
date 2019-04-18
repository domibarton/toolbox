# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from datetime import date
from .models import Order, State
from .forms import OrderCreateForm, OrderUpdateForm
from .post import TrackAndTrace
from toolbox.settings import SHIPPING_STATUS_DELIVERED


class OrderListView(ListView):
    model = Order

    def get_context_data(self):
        context           = super(OrderListView, self).get_context_data()
        context['states'] = State.objects.all()
        return context

    def post(self, request):
        update_state = self.request.POST.get('update-state')
        update_order = self.request.POST.get('update-order')
        order_ids    = self.request.POST.getlist('id[]')

        orders = Order.objects.filter(pk__in=order_ids)

        if update_state:
            state = State.objects.get(pk=int(update_state))
            orders.update(state=state)

        if update_order:
            if 'complete' in update_order:
                orders.update(complete=True)

            if 'delivered' in update_order:
                orders.filter(delivery_date=None).update(delivery_date=date.today())

            if 'shipped' in update_order:
                orders.filter(shipping_date=None).update(shipping_date=date.today())
                return redirect('ordertracking:update-shipping-nr', pks=','.join(order_ids))

        return redirect(request.META.get('HTTP_REFERER') or 'ordertracking:list')


class OrderIncompleteListView(OrderListView):

    def get_queryset(self):
        return super(OrderIncompleteListView, self).get_queryset().filter(complete=False)

    def get_context_data(self):
        context               = super(OrderIncompleteListView, self).get_context_data()
        context['incomplete'] = True
        return context


class OrderModalView(DetailView):
    model = Order


class OrderCreateView(CreateView):
    model       = Order
    form_class  = OrderCreateForm
    success_url = reverse_lazy('ordertracking:list')


class OrderUpdateView(UpdateView):
    model       = Order
    form_class  = OrderUpdateForm
    success_url = reverse_lazy('ordertracking:list')


class OrderUpdateShippingNrView(ListView):
    model                = Order
    template_name_suffix = '_shipping_nr_list'

    def get_queryset(self):
        pks = self.kwargs['pks'].split(',')
        qs  = self.model.objects.filter(pk__in=pks)
        return qs

    def post(self, request, pks):
        order_ids    = [int(i) for i in self.request.POST.getlist('id[]')]
        shipping_nrs = self.request.POST.getlist('shipping-nr[]')

        mapping = {}
        i       = 0
        for order_id in order_ids:
            mapping[order_id] = shipping_nrs[i]
            i                 += 1

        for order in self.get_queryset():
            shipping_nr = mapping[order.id].strip()
            if shipping_nr:
                order.shipping_nr = shipping_nr
                order.save()

        return redirect('ordertracking:list')


class OrderUpdateShippingStatusView(ListView):
    model = Order

    def get_queryset(self):
        '''
        Returns only incomplete orders with a shipping number.
        '''
        qs = super(OrderUpdateShippingStatusView, self).get_queryset()
        return qs.filter(complete=False).exclude(shipping_nr='')

    def get(self, request):
        '''

        '''
        orders = {o.shipping_nr: o for o in self.get_queryset()}

        if orders:
            for n, e in TrackAndTrace.get_shipping_events(orders.keys()).iteritems():
                o = orders[n]
                o.shipping_status = e
                if e in SHIPPING_STATUS_DELIVERED and not o.delivery_date:
                    o.delivery_date = date.today()
                o.save()

        return redirect(request.META.get('HTTP_REFERER') or 'home')
