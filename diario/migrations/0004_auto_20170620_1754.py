# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 20:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0003_auto_20170605_1754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pesquisa',
            options={'ordering': ('data',), 'verbose_name': 'Pesquisa', 'verbose_name_plural': 'Pesquisas'},
        ),
        migrations.RemoveField(
            model_name='pesquisa',
            name='busca_arquivo',
        ),
    ]
