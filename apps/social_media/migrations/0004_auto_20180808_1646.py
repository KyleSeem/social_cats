# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-08 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0003_auto_20180808_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelTable(
            name='post',
            table=None,
        ),
    ]