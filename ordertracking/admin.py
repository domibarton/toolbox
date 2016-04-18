# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import State, Store, Order


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
        'arrival_date',
        'state',
        'complete',
    )

    list_filter = (
        'store',
        'state',
        'complete',
        'order_date',
        'shipping_date',
        'arrival_date',
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
                'arrival_date',
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

admin.site.register(State, StateAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Order, OrderAdmin)
