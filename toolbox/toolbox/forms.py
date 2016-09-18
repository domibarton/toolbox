# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class ToolboxAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(ToolboxAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'login', css_class='btn green pull-right'))


class ToolboxPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(ToolboxPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'change password', css_class='btn green'))
