from django.db import models
from cliente.models import Cliente
from controle_usuario.models import funcionario


class Processo(models.Model):

    numero_acervo   = models.CharField(max_length=1000)
    numero_processo = models.CharField(max_length=1000)
    data_abertura   = models.DateTimeField(blank=True)
    comarca         = models.CharField(max_length=1000)
    assistencia_judiciaria = models.CharField(max_length=1000)
    natureza        = models.CharField(max_length=1000)
    classe_processual = models.CharField(max_length=1000)
    assuntos        = models.CharField(max_length=1000)
    observacao      = models.CharField(max_length=1000)
    valor_acao      = models.CharField(max_length=1000)
    status_atual    = models.CharField(max_length=1000)
    status_processo = models.BooleanField()
    cliente         = models.ForeignKey(Cliente, null=True, blank=True)
    usuario         = models.ForeignKey(funcionario, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Partes(models.Model):

    processo  = models.ForeignKey(Processo)
    parte     = models.CharField(max_length=1000)
    descricao = models.CharField(max_length=1000)


class Movimento(models.Model):

    processo          = models.ForeignKey(Processo)
    data_movimentacao = models.DateTimeField(blank=True)
    descricao         = models.TextField(max_length=1000)
    doc = models.FileField(blank=True, null=True)

    class Meta:
        ordering = ('-data_movimentacao',)


class Distribuicao(models.Model):

    processo   = models.ForeignKey(Processo)
    realizada  = models.DateTimeField(blank=True)
    tipo_distribuicao = models.CharField(max_length=1000)
    comarca    = models.CharField(max_length=1000)
    secretaria = models.CharField(max_length=1000)
    motivo     = models.TextField(max_length=1000)
