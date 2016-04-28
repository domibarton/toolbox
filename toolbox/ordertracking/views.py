# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from datetime import date
from .models import Order, Store, State


class OrderListView(ListView):
    model = Order


class OrderDetailView(DetailView):
    model = Order


class OrderCompleteView(View):
    model = Order

    def get(self, request,  *args, **kwargs):
        order = get_object_or_404(Order, complete=False, pk=self.kwargs['pk'])

        order.complete = True
        if not order.delivery_date:
            order.delivery_date = date.today()
        order.save()

        if 'HTTP_REFERER' in request.META:
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect('ordertracking:list')
