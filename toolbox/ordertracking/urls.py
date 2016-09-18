# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import OrderListView, OrderDetailView

urlpatterns = [
    url(
        regex=r'^$',
        view=OrderListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/details/$',
        view=OrderDetailView.as_view(),
        name='detail'
    ),
]
