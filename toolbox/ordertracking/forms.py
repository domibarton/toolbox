# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from django.forms import ModelForm
from .models import Order


class OrderCreateForm(ModelForm):

    class Meta:

        model = Order

        fields = (
            'store',
            'order_id',
            'brief',
            'description',
            'order_date',
            'state',
        )

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.helper        = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('store', css_class='col-md-6'),
                Div('order_id', css_class='col-md-6'),
                css_class='row'
            ),
            'brief',
            'description',
            Div(
                Div('order_date', css_class='col-md-6'),
                Div('state', css_class='col-md-6'),
                css_class='row'
            ),
            ButtonHolder(
                Submit('submit', 'create order', css_class='btn green-meadow')
            )
        )


class OrderUpdateForm(ModelForm):

    class Meta:

        model = Order

        fields = (
            'store',
            'order_id',
            'shipping_nr',
            'brief',
            'description',
            'notes',
            'order_date',
            'shipping_date',
            'delivery_date',
            'complete',
            'state',
        )

    def __init__(self, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
        self.helper        = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('store', css_class='col-md-4'),
                Div('order_id', css_class='col-md-4'),
                Div('shipping_nr', css_class='col-md-4'),
                css_class='row'
            ),
            'brief',
            'description',
            'notes',
            Div(
                Div('order_date', css_class='col-md-4'),
                Div('shipping_date', css_class='col-md-4'),
                Div('delivery_date', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('complete', css_class='col-md-6'),
                Div('state', css_class='col-md-6'),
                css_class='row'
            ),
            ButtonHolder(
                Submit('submit', 'edit order', css_class='btn green-meadow')
            )
        )