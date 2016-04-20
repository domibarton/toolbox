# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import OrderListView, OrderDetailView, OrderCompleteView

urlpatterns = [
    url(
        regex=r'^$',
        view=OrderListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=OrderDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^(?P<pk>\d+)/complete/$',
        view=OrderCompleteView.as_view(),
        name='complete'
    ),
]
