# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20170612_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='video_url',
            field=models.CharField(max_length=10000),
        ),
    ]
