# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prngmgr', '0003_remove_peeringsession_general_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='peeringsession',
            name='accepted_prefixes',
            field=models.IntegerField(default=0),
        ),
    ]
