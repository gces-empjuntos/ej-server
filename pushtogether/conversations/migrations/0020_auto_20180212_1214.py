# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-12 10:15
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0019_auto_20180212_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_caption',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
