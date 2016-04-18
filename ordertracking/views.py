# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Order, Store, State


class OrderListView(ListView):
    model = Order


class OrderDetailView(DetailView):
    model = Order
