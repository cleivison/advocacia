# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .choices import UF
from django.contrib.auth.models import User
from cliente.models import Cliente
from controle_usuario.models import funcionario

class Evento(models.Model):

    id_evento = models.AutoField(_('id'), primary_key=True)
    cliente   = models.ForeignKey(Cliente, null = True, blank = True)
    usuario   = models.ForeignKey(funcionario, null = True, blank = True)
    titulo    = models.CharField(_('Titulo'), max_length=60)
    data      = models.DateField(blank=False, null=False)
    hora      = models.TimeField(_('Hora'), blank=False, null=True)
    endereco  = models.CharField(_('Endereço'), max_length=80, blank=True, null=True)
    uf        = models.CharField( _('UF'), max_length=2, blank=True, null=True, choices=UF)
    telefone  = models.CharField(_('Telefone'), max_length=20, blank=True, null=True)
    email     = models.EmailField(_('E-mail'), max_length=300, blank=True, null=True)
    bairro    = models.CharField(_('Bairro'), max_length=20, blank=True, null=True)
    anotacao  = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('data',)
        verbose_name = _('Evento')
        verbose_name_plural = _('Eventos')

    def __str__(self):
        return self.titulo
