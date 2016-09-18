# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
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
            if update_date == 'shipped':
                orders.filter(shipping_date=None).update(shipping_date=date.today())

            if update_date in ('delivered', 'complete'):
                orders.filter(delivery_date=None).update(delivery_date=date.today())

            if update_date == 'complete':
                orders.update(complete=True)

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
