# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-08 16:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0002_auto_20180808_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
