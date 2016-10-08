# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_handleref.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_peeringdb', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeeringRouter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=255, verbose_name='Status', blank=True)),
                ('created', django_handleref.models.CreatedDateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', django_handleref.models.UpdatedDateTimeField(auto_now=True, verbose_name='Updated')),
                ('version', models.IntegerField(default=0)),
                ('hostname', models.CharField(unique=True, max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PeeringRouterIXInterface',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=255, verbose_name='Status', blank=True)),
                ('created', django_handleref.models.CreatedDateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', django_handleref.models.UpdatedDateTimeField(auto_now=True, verbose_name='Updated')),
                ('version', models.IntegerField(default=0)),
                ('netixlan', models.OneToOneField(related_name='+', null=True, default=0, to='django_peeringdb.NetworkIXLan')),
                ('prngrtr', models.ForeignKey(related_name='prngrtriface_set', default=0, to='prngmgr.PeeringRouter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PeeringSession',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=255, verbose_name='Status', blank=True)),
                ('created', django_handleref.models.CreatedDateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', django_handleref.models.UpdatedDateTimeField(auto_now=True, verbose_name='Updated')),
                ('version', models.IntegerField(default=0)),
                ('provisioning_state', models.IntegerField(default=0, choices=[(0, None), (1, b'pending'), (2, b'complete')])),
                ('admin_state', models.IntegerField(default=0, choices=[(0, None), (1, b'stop'), (2, b'start')])),
                ('operational_state', models.IntegerField(default=0, choices=[(0, None), (1, b'idle'), (2, b'connect'), (3, b'active'), (4, b'opensent'), (5, b'openconfirm'), (6, b'established')])),
                ('af', models.IntegerField(default=0, choices=[(0, b'unknown'), (1, b'ipv4'), (2, b'ipv6')])),
                ('peer_netixlan', models.ForeignKey(related_name='+', default=0, to='django_peeringdb.NetworkIXLan', null=True)),
                ('prngrtriface', models.ForeignKey(related_name='prngsess_set', default=0, to='prngmgr.PeeringRouterIXInterface')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='peeringsession',
            unique_together=set([('af', 'prngrtriface', 'peer_netixlan')]),
        ),
    ]
