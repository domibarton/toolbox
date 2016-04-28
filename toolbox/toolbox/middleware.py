# -*- coding: utf-8 -*-
'''
Definition of all project specific middleware classes.
'''

import re
from .settings import LOGIN_REQUIRED_URLS, LOGIN_REQUIRED_URLS_EXCEPTIONS
from django.contrib.auth.decorators import login_required


class LoginRequiredMiddleware(object):
    '''
    Middleware class which wraps Django's own login_required decorator
    (django.contrib.auth.decorators.login_required) around configured URL
    patterns.

    The configuration of the URL patterns are defined in the settings module.
    Here's an example of that configuration:

        LOGIN_REQUIRED_URLS = (
            r'^/private/.*',
        )

        LOGIN_REQUIRED_URLS_EXCEPTIONS = (
            r'^/private/and-still-public/$',
        )

    Please note all URL patterns have to be a valid regular expressions.
    '''

    def __init__(self):
        self.required   = tuple(re.compile(url) for url in LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url) for url in LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip is user is already authenticated.
        if request.user.is_authenticated():
            return None

        # Handle all exceptions.
        for url in self.exceptions:
            if url.search(request.path):
                return None

        # Handle required authentication patterns.
        for url in self.required:
            print url.search(request.path)
            if url.search(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)

        print request.path
        return None
