# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, verbose_name='Texto '),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=200, verbose_name='Titulo '),
        ),
    ]
