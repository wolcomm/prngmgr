# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prngmgr', '0002_auto_20161005_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peeringsession',
            name='general_state',
        ),
    ]
