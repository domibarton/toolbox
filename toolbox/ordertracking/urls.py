# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        regex=r'^$',
        view=OrderIncompleteListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^all/$',
        view=OrderListView.as_view(),
        name='list-all'
    ),
    url(
        regex=r'^create/$',
        view=OrderCreateView.as_view(),
        name='create'
    ),
    url(
        regex=r'^(?P<pk>\d+)/modal/$',
        view=OrderModalView.as_view(),
        name='modal'
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=OrderUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^(?P<pks>[0-9,]+)/update-shipping-nr/$',
        view=OrderUpdateShippingNrView.as_view(),
        name='update-shipping-nr'
    ),
    url(
        regex=r'^update-shipping-status/$',
        view=OrderUpdateShippingStatusView.as_view(),
        name='update-shipping-status'
    ),
]
