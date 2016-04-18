# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from toolbox.settings import LOGIN_REDIRECT_URL
from .views import IndexView

urlpatterns = [
    url(
        regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': LOGIN_REDIRECT_URL},
        name='logout'
    ),
    url(
        regex=r'^$',
        view=IndexView.as_view(),
        name='index',
    ),
    url(
        regex=r'^admin/',
        view=admin.site.urls
    ),
    url(
        regex=r'^ordertracking/',
        view=include('ordertracking.urls', namespace='ordertracking')
    ),
]
