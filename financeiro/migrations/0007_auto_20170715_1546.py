# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-15 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0006_conta_receber_processo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='n_parcela',
            field=models.IntegerField(blank=True, choices=[(0, 'Escolha uma opção'), (1, '1x'), (2, '2x'), (3, '3x'), (4, '4x'), (5, '5x'), (6, '6x'), (7, '7x'), (8, '8x'), (9, '9x'), (10, '10x'), (11, '11x'), (12, '12x')], default=1, verbose_name='Nº Da Parcela'),
        ),
    ]
