# -*- coding: utf-8 -*-
'''
Definition of all HACTAR core related forms.

Django provides a lot of tools and libraries to work with data inputs received
by the user. Forms are a big part of these libraries and they'll help you to
render, validate and save forms based on models. More about working with Django
forms can be found here:

https://docs.djangoproject.com/en/1.9/topics/forms/

Because we're using a Twitter Bootstrap theme we're not able to use Django's
stock forms and we're using a great alternative called Crispy Forms. With
Crispy Forms we can render forms in a Bootstrap-compliant way and even enhance
them to our desired look and feel. More about Crispy Forms here:

http://django-crispy-forms.readthedocs.org/en/latest/

Copyright © 2016 confirm IT solutions
'''

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class ToolboxAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(ToolboxAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'login', css_class='btn success pull-right'))


class ToolboxPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(ToolboxPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'change password', css_class='btn success'))
