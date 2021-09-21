# -*- coding: utf-8 -*-
from django.db import models
from .choices import UF, PONTO, SEXO


# https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
class Cliente(models.Model):
    nome       = models.CharField('Nome', max_length=60)
    cpf        = models.CharField('CPF', max_length=14,unique=True, null=True, blank=True)
    sexo       = models.CharField('Sexo', max_length=1, choices=SEXO, blank=True)
    apelido    = models.CharField(max_length=30,blank=True)
    nascimento = models.DateField('Data Nascimento')
    email      = models.EmailField('E-mail', max_length=300)
    rua        = models.CharField('Rua', max_length=1000)
    bairro     = models.CharField('Bairro', max_length=100, blank=True, null=True)
    complemento = models.CharField(max_length=50,blank=True)
    uf         = models.CharField('UF', max_length=2, choices=UF)
    cep        = models.CharField('CEP', max_length=20, blank=True)
    criado_em  = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now_add=True)
    numero1    = models.CharField('Telefone Principal', max_length=20)
    numero2    = models.CharField('Telefone 2', max_length=20, blank=True)

  
    class Meta:
        ordering = ('-nome',)
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome +' ' + self.cpf 


class Trabalhista(models.Model):
    cliente     = models.ForeignKey(Cliente)
    ctps        = models.CharField('CTPS', max_length=15)
    admissao    = models.DateField('Admissão')
    demissao    = models.DateField('Demissão')
    recisao     = models.DateField('Recisão')
    salario     = models.CharField('Salário', max_length=20)
    funcao      = models.CharField('Função', max_length=100)
    entrada_manha = models.TimeField('Entrada(M)')
    saida_manha = models.TimeField('Saída(M)')
    entrada_tarde = models.TimeField('Entrada(T)')
    saida_tarde = models.TimeField('Saída(T)')
    seg = models.BooleanField('Seg')
    ter = models.BooleanField('Ter')
    qua = models.BooleanField('Qua')
    qui = models.BooleanField('Qui')
    sex = models.BooleanField('Sex')
    sab = models.BooleanField('Sáb')
    dom = models.BooleanField('Dom')
    obs_semana = models.TextField('Observação Horário')
    hor_con   = models.BooleanField('Controle de horário')
    ponto     = models.CharField('Ponto', max_length=100, choices=PONTO)
    obs_ponto = models.TextField('Observação Ponto')
    pergunta1 = models.CharField('Quem marcava o ponto', max_length=100)
    pergunta2 = models.BooleanField('Marcava no mesmo horário')
    pergunta3 = models.BooleanField('Marcava o horário correto')
    hora_intineri = models.BooleanField('Hora Intineri')

    class Meta:
        verbose_name = 'Trabalhista'
        verbose_name_plural = 'Trabalhistas'

    def __str__(self):
        return self.ctps
class Documentos(models.Model):
    cliente = models.ForeignKey(Cliente)
    doc     = models.FileField(verbose_name='', blank=True, null=True,upload_to='documents/%Y/%m/%d/')
    class Meta:
        verbose_name='Documento'
        verbose_name_plural = 'Documentos'

    def doc_name(self):
        return self.doc.name[10:]

   