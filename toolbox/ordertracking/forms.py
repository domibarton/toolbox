# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, HTML, Div
from django.forms import ModelForm
from .models import Order


class OrderCreateForm(ModelForm):

    class Meta:

        model = Order

        fields = (
            'store',
            'order_id',
            'shipping_nr',
            'brief',
            'description',
            'price',
            'order_date',
            'state',
        )

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.helper        = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('store', css_class='col-md-4'),
                Div('order_id', css_class='col-md-4'),
                Div('shipping_nr', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('brief', css_class='col-md-8'),
                Div('price', css_class='col-md-4'),
                css_class='row'
            ),
            'description',
            Div(
                Div('order_date', css_class='col-md-6'),
                Div('state', css_class='col-md-6'),
                css_class='row'
            ),
            ButtonHolder(
                HTML('<button role="submit" class="btn btn green-meadow"><i class="fa fa-check"></i> create order</button>'),
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
            'price',
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
            Div(
                Div('brief', css_class='col-md-8'),
                Div('price', css_class='col-md-4'),
                css_class='row'
            ),
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
                HTML('<button role="submit" class="btn btn green-meadow"><i class="fa fa-check"></i> edit order</button>'),
            )
        )
