# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prngmgr', '0006_auto_20161008_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peeringsession',
            name='previous_state',
            field=models.CharField(default=b'None', max_length=12),
        ),
    ]
