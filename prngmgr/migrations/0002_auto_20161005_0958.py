# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_peeringdb', '__first__'),
        ('prngmgr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternetExchangeProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_peeringdb.internetexchange',),
        ),
        migrations.CreateModel(
            name='NetworkProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_peeringdb.network',),
        ),
        migrations.AddField(
            model_name='peeringsession',
            name='general_state',
            field=models.IntegerField(default=0, choices=[(0, None), (1, b'Provisioning'), (2, b'Admin Down'), (3, b'Down'), (4, b'Up')]),
        ),
    ]
