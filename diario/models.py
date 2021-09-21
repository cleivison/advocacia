from django.db import models


class Pesquisa(models.Model):
    nome_arquivo  = models.CharField('Nome arquivo', max_length=100)
    busca_diario  = models.CharField('Busca diario', max_length=100)
    data          = models.DateTimeField('data', max_length=100)
    tipo          = models.CharField('Tipo', max_length=100)
    class Meta:

        verbose_name = 'Pesquisa'
        verbose_name_plural = 'Pesquisas'

    def __str__(self):
        return self.nome_arquivo +' ' + self.data