from django.db import models
from cliente.models import Cliente
from controle_usuario.models import funcionario


class Processo_trabalhista(models.Model):

    numero_processo          = models.CharField(max_length=1000)
    ano_processo             = models.CharField(blank=True, max_length=10)
    VVV                      = models.CharField(max_length=1000)
    RR                       = models.CharField(max_length=1000)
    SS                       = models.CharField(max_length=1000)
    especie                  = models.CharField(max_length=1000)
    reclamante               = models.CharField(max_length=1000)
    advogado_reclamante      = models.CharField(max_length=1000)
    reclamado                = models.CharField(max_length=1000)
    advogado_reclamado       = models.CharField(max_length=1000)
    etapa_processo           = models.CharField(max_length=1000)
    cliente         = models.ForeignKey(Cliente, null=True, blank=True)
    usuario         = models.ForeignKey(funcionario, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Movimento_trab(models.Model):

    processo          = models.ForeignKey(Processo_trabalhista)
    data_movimentacao = models.DateField(blank=True)
    descricao         = models.TextField(max_length=1000)
    doc = models.FileField(blank=True, null=True)

    class Meta:
        ordering = ('-data_movimentacao',)