# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-03 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0009_auto_20190329_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='wait_for_files',
            field=models.BooleanField(default=False, help_text=b'Wait for files, use this if the cluster is not syncing files beforerunning the job and causing errors.'),
        ),
    ]
