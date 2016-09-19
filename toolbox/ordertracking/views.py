# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_list_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from datetime import date
from .models import Order, Store, State
from .forms import OrderCreateForm, OrderUpdateForm


class OrderListView(ListView):
    model = Order

    def get_context_data(self):
        context           = super(OrderListView, self).get_context_data()
        context['states'] = State.objects.all()
        return context

    def post(self, request):
        update_state = self.request.POST.get('update-state')
        update_date  = self.request.POST.get('update-date')
        order_ids    = self.request.POST.getlist('id[]')

        orders = Order.objects.filter(pk__in=order_ids)

        if update_state:
            state = State.objects.get(pk=int(update_state))
            orders.update(state=state)

        if update_date:
            if update_date == 'complete':
                orders.update(complete=True)

            if update_date in ('delivered', 'complete'):
                orders.filter(delivery_date=None).update(delivery_date=date.today())

            if update_date == 'shipped':
                orders.filter(shipping_date=None).update(shipping_date=date.today())
                return redirect('ordertracking:update-shipping-nr', pks=','.join(order_ids))

        return redirect('ordertracking:list')


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
