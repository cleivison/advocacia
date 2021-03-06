# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170415_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Detail Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Texto'),
        ),
    ]
