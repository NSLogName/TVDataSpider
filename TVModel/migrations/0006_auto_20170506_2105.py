# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TVModel', '0005_auto_20170506_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programdetail',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='programdetail',
            name='menu',
            field=models.TextField(),
        ),
    ]
