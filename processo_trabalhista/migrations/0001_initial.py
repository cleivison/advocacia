# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 23:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0002_auto_20170504_2223'),
        ('controle_usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movimento_trab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_movimentacao', models.DateTimeField(blank=True)),
                ('descricao', models.TextField(max_length=1000)),
                ('doc', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'ordering': ('-data_movimentacao',),
            },
        ),
        migrations.CreateModel(
            name='Processo_trabalhista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_processo', models.CharField(max_length=1000)),
                ('ano_processo', models.DateTimeField(blank=True)),
                ('VVV', models.CharField(max_length=1000)),
                ('RR', models.CharField(max_length=1000)),
                ('SS', models.CharField(max_length=1000)),
                ('especie', models.CharField(max_length=1000)),
                ('reclamante', models.CharField(max_length=1000)),
                ('advogado_reclamante', models.CharField(max_length=1000)),
                ('reclamado', models.CharField(max_length=1000)),
                ('advogado_reclamado', models.CharField(max_length=1000)),
                ('etapa_processo', models.CharField(max_length=1000)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='controle_usuario.funcionario')),
            ],
        ),
        migrations.AddField(
            model_name='movimento_trab',
            name='processo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processo_trabalhista.Processo_trabalhista'),
        ),
    ]
