# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-11-07 18:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_auto_20170202_1539'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='place',
            unique_together=set([('name', 'country')]),
        ),
    ]