# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TVModel', '0002_auto_20170506_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='programdetail',
            name='name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
