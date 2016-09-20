# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change, password_change_done
from toolbox.settings import LOGIN_REDIRECT_URL
from .views import HomeView
from .forms import ToolboxAuthenticationForm, ToolboxPasswordChangeForm

urlpatterns = [
    url(
        regex=r'^admin/',
        view=admin.site.urls
    ),
    url(
        regex=r'^login/$',
        view=login,
        kwargs={
            'authentication_form': ToolboxAuthenticationForm,
            'template_name': 'toolbox/login.html',
        },
        name='login'
    ),
    url(
        regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': LOGIN_REDIRECT_URL},
        name='logout'
    ),
    url(
        regex=r'^password_change/$',
        view=password_change,
        kwargs={
            'password_change_form': ToolboxPasswordChangeForm,
            'template_name': 'toolbox/password_change_form.html',
        },
        name='password_change'
    ),
    url(
        regex=r'^password_change/$',
        view=password_change_done,
        kwargs={
            'template_name': 'toolbox/password_change_form.html',
            'extra_context': {'password_changed': True}
        },
        name='password_change_done'
    ),
    url(
        regex=r'^$',
        view=HomeView.as_view(),
        name='home',
    ),
    url(
        regex=r'^ordertracking/',
        view=include('ordertracking.urls', namespace='ordertracking')
    ),
    url(
        regex=r'^rchobby/',
        view=include('rchobby.urls', namespace='rchobby')
    ),
]
