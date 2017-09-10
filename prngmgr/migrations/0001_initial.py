# -*- coding: utf-8 -*-
# Copyright 2016-2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Intial database migration for prngmgr."""

from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    """Initial migrations for prngmgr models."""

    initial = True

    dependencies = [
        ('django_peeringdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeeringRouter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeeringRouterIXInterface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('netixlan', models.OneToOneField(
                    default=0, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='prngrtriface_set',
                    to='django_peeringdb.NetworkIXLan')),
                ('prngrtr', models.ForeignKey(
                    default=0,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='prngrtriface_set',
                    to='prngmgr.PeeringRouter')),
            ],
        ),
        migrations.CreateModel(
            name='PeeringSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('provisioning_state', models.IntegerField(
                    choices=[(0, None), (1, b'pending'), (2, b'complete')],
                    default=0)),
                ('admin_state', models.IntegerField(
                    choices=[(0, None), (1, b'stop'), (2, b'start')],
                    default=0)),
                ('operational_state', models.IntegerField(
                    choices=[
                        (0, None), (1, b'idle'), (2, b'connect'),
                        (3, b'active'), (4, b'opensent'),
                        (5, b'openconfirm'), (6, b'established')],
                    default=0)),
                ('af', models.IntegerField(
                    choices=[(0, b'unknown'), (1, b'ipv4'), (2, b'ipv6')],
                    default=0)),
                ('accepted_prefixes', models.IntegerField(default=None,
                                                          null=True)),
                ('previous_state', models.CharField(default=b'None',
                                                    max_length=12)),
                ('state_changed', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('peer_netixlan', models.ForeignKey(
                    default=0, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='prngsess_set',
                    to='django_peeringdb.NetworkIXLan')),
                ('prngrtriface', models.ForeignKey(
                    default=0, on_delete=django.db.models.deletion.CASCADE,
                    related_name='prngsess_set',
                    to='prngmgr.PeeringRouterIXInterface')),
            ],
        ),
        migrations.CreateModel(
            name='InternetExchangeProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('django_peeringdb.internetexchange',),
        ),
        migrations.CreateModel(
            name='NetworkProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('django_peeringdb.network',),
        ),
        migrations.AlterUniqueTogether(
            name='peeringsession',
            unique_together=set([('af', 'prngrtriface', 'peer_netixlan')]),
        ),
    ]
