# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import State, Store, Order
from datetime import date
from collections import OrderedDict


class StateAdmin(admin.ModelAdmin):

    list_display = (
        'state',
        'sort',
    )


class StoreAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'order_url',
    )


class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'order_id',
        'store',
        'brief',
        'order_date',
        'shipping_date',
        'delivery_date',
        'state',
        'complete',
    )

    list_filter = (
        'store',
        'state',
        'complete',
        'order_date',
        'shipping_date',
        'delivery_date',
    )

    search_fields = (
        'store__name',
        'order_id',
        'brief',
    )

    fieldsets = (
        ('Order', {
            'fields': (
                'store',
                'order_id',
                'shipping_nr',
                'state',
                'complete',
            )
        }),
        ('Dates', {
            'fields': (
                'order_date',
                'shipping_date',
                'delivery_date',
            )
        }),
        ('Description', {
            'fields': (
                'brief',
                'description',
            )
        }),
        ('Notes', {
            'fields': (
                'notes',
            )
        }),
    )

    actions = (
        'set_complete_delivered',
        'set_complete',
        'set_incomplete',
        'set_shipped',
        'set_delivered',
    )

    def set_complete_delivered(self, request, queryset):
        self.set_complete(request, queryset)
        self.set_delivered(request, queryset)
    set_complete_delivered.short_description = 'Mark selected orders as complete and set states to "delivered"'

    def set_complete(self, request, queryset):
        queryset.update(complete=True)
        self.set_delivered(request, queryset)
    set_complete.short_description = 'Mark selected orders as complete'

    def set_incomplete(self, request, queryset):
        queryset.update(complete=False)
    set_incomplete.short_description = 'Mark selected orders as incomplete'

    def set_shipped(self, request, queryset):
        queryset.filter(shipping_date=None).update(shipping_date=date.today())
    set_shipped.short_description = 'Set shipping date of selected orders to today'

    def set_delivered(self, request, queryset):
        queryset.filter(delivery_date=None).update(delivery_date=date.today())
    set_delivered.short_description = 'Set delivery date of selected orders to today'

    def make_state_action(self, state):
        name   = 'set_state_{0}'.format(state.state)
        desc   = 'Set state of selected orders to "{}"'.format(state.state)
        action = lambda ma, req, qs: qs.update(state=state)
        return (name, (action, name, desc))

    def get_actions(self, request):
        actions       = super(OrderAdmin, self).get_actions(request)
        state_actions = OrderedDict((self.make_state_action(s) for s in State.objects.all()))
        actions.update(state_actions)
        return actions

admin.site.register(State, StateAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Order, OrderAdmin)
