# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prngmgr', '0005_auto_20161008_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='peeringsession',
            name='previous_state',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='peeringsession',
            name='state_changed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
