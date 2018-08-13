# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-08 18:25
from __future__ import unicode_literals

import apps.social_media.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0005_auto_20180808_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='user',
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(upload_to=apps.social_media.models.upload_path),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
