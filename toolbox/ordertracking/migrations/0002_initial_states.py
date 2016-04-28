# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


def create_states(apps, schema_editor):
    State = apps.get_model('ordertracking', 'State')
    db_alias = schema_editor.connection.alias
    State.objects.using(db_alias).bulk_create([
        State(state='normal', sort=1),
        State(state='backorder', sort=2),
        State(state='issue', sort=3),
        State(state='lost', sort=4),
        State(state='refund', sort=5),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('ordertracking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_states),
    ]
