# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        regex=r'^$',
        view=IndexView.as_view(),
        name='index'
    ),
    url(
        regex=r'^hyperion/$',
        view=HyperionView.as_view(),
        name='hyperion'
    ),
]
