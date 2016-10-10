# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prngmgr', '0007_auto_20161008_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peeringrouter',
            name='created',
        ),
        migrations.RemoveField(
            model_name='peeringrouter',
            name='status',
        ),
        migrations.RemoveField(
            model_name='peeringrouter',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='peeringrouter',
            name='version',
        ),
        migrations.RemoveField(
            model_name='peeringrouterixinterface',
            name='created',
        ),
        migrations.RemoveField(
            model_name='peeringrouterixinterface',
            name='status',
        ),
        migrations.RemoveField(
            model_name='peeringrouterixinterface',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='peeringrouterixinterface',
            name='version',
        ),
        migrations.RemoveField(
            model_name='peeringsession',
            name='created',
        ),
        migrations.RemoveField(
            model_name='peeringsession',
            name='status',
        ),
        migrations.RemoveField(
            model_name='peeringsession',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='peeringsession',
            name='version',
        ),
        migrations.AlterField(
            model_name='peeringrouter',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='peeringrouterixinterface',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='peeringsession',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
