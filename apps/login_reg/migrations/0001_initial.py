# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-12 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('pw_hashed', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('userManager', django.db.models.manager.Manager()),
            ],
        ),
    ]
