# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2022-08-04 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Libsys', '0003_auto_20220803_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('admin', 'admin'), ('moderator', 'moderator')], max_length=30),
        ),
        migrations.DeleteModel(
            name='UserRoles',
        ),
    ]
