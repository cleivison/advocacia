# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm,TextInput,DateInput,Select,EmailInput
from django.utils.translation import ugettext_lazy as _

from .models import Evento

class EventoForm(ModelForm):

    class Meta:
        model = Evento
        exclude = ['id_evento']
        widgets = {
                'titulo': TextInput(attrs={'class': 'form-control'}),
                'data': DateInput(attrs={'class': 'form-control datepicker-here','data-language': 'pt'}),
                'hora':TextInput(attrs={'class':'form-control'}),
                'email':EmailInput(attrs={'class':'form-control'}),
                'rua':TextInput(attrs={'class':'form-control'}),
                'endereco':TextInput(attrs={'class':'form-control'}),
                'telefone':TextInput(attrs={'class':'form-control'}),
                'bairro':TextInput(attrs={'class':'form-control','placeholder':' Ex, Bairro piaui'}),
                'uf':Select(attrs={'class':'form-control'}),
                'usuario':Select(attrs={'class':'form-control'}),
                'cliente':Select(attrs={'class':'form-control'}),
            }