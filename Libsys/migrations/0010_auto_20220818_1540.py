# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2022-08-18 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Libsys', '0009_auto_20220818_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.AutoField(default=True, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='aadhar_id',
            field=models.CharField(max_length=16),
        ),
    ]
