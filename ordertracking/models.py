# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from datetime import date
from toolbox.settings import SHIPPING_URL


class State(models.Model):
    state    = models.CharField(max_length=16, unique=True)
    sort     = models.IntegerField(db_index=True)

    def __unicode__(self):
        return self.state

    class Meta:
        ordering = (
            'sort',
        )


class Store(models.Model):
    name      = models.CharField(max_length=32, unique=True)
    order_url = models.CharField(max_length=255, db_index=True, verbose_name='order URL')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = (
            'name',
        )


class Order(models.Model):
    store         = models.ForeignKey(Store)
    state         = models.ForeignKey(State, default=1)
    order_id      = models.CharField(max_length=24, db_index=True, verbose_name='order ID')
    shipping_nr   = models.CharField(max_length=32, null=True, blank=True, verbose_name='shipping number')
    brief         = models.CharField(max_length=255, db_index=True)
    description   = models.TextField(null=True, blank=True)
    notes         = models.TextField(null=True, blank=True)
    order_date    = models.DateField(db_index=True, default=date.today)
    shipping_date = models.DateField(db_index=True, null=True, blank=True)
    arrival_date  = models.DateField(db_index=True, null=True, blank=True)
    complete      = models.BooleanField(db_index=True, default=False)

    def __unicode__(self):
        return '{} {}'.format(self.store, self.order_id)

    def get_absolute_url(self):
        return reverse('ordertracking:detail', kwargs={'pk': self.id})

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def get_shipping_url(self):
        return SHIPPING_URL.format(self.shipping_nr)

    def get_order_url(self):
        return self.store.order_url.format(self.order_id)

    def get_duration_days(self):
        if self.arrival_date:
            return (self.arrival_date - self.order_date).days
        else:
            return (date.today() - self.order_date).days

    class Meta:
        ordering = (
            '-order_date',
            '-id',
        )

        unique_together = (
            ('store', 'order_id'),
        )
