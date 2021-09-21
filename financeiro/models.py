# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .choices import pagamentos
from .choices import parcelas
from processos.models import Processo


class Categoria(models.Model):

    desc = models.CharField(verbose_name='Descrição', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')

    def __str__(self):
        return str(self.desc)

class Conta(models.Model):

    vencimento    = models.DateField(blank=False, null=True)
    valor_total   = models.CharField(null=False, blank=False,max_length=20)
    n_parcela     = models.IntegerField(default=1, choices=parcelas,blank=True,verbose_name="Nº Da Parcela")
    status_pag    = models.BooleanField(default=False)
    forma_pagamento = models.CharField(max_length=100, null=False, blank=False, choices=pagamentos)
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    valor_entrada = models.CharField(default = 0,null=False, blank=False,max_length=20)
    valor_parcela = models.CharField(default = 0,null=False, blank=False,max_length=20)
    categoria     = models.ForeignKey(Categoria, null=True, blank=True)

    class Meta:
        ordering = ('-vencimento',)
        verbose_name = _('Conta')
        verbose_name_plural = _('Contas')

    def __str__(self):
        return str(self.id)


class Conta_receber(Conta):

    descricao  = models.TextField(verbose_name='Descrição',max_length=200, null=True, blank=True)
    observacao = models.TextField(verbose_name='Observação', max_length=200, null=True, blank=True)
    processo = models.ForeignKey(Processo, null=True, blank=True)

    class Meta:
        verbose_name = _('Conta à receber')
        verbose_name_plural = _('Contas à receber')


class Conta_pagar(Conta):
    conta_fixa = models.NullBooleanField(default=False)
    descricao  = models.TextField(verbose_name='Descrição',max_length=200, null=True, blank=True)
    observacao = models.TextField(verbose_name='Observação',max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('Conta à pagar')
        verbose_name_plural = _('Contas à pagar')


class Parcela(models.Model):

    conta      = models.ForeignKey(Conta)
    vencimento = models.DateField(blank=False, null=False)
    status_pag = models.BooleanField(default=False)
    data_pag   = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _('Parcela')
        verbose_name_plural = _('Parcelas')

    def __str__(self):
        return str(self.id) + str(self.vencimento)

