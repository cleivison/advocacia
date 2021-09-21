from django.forms import ModelForm,RadioSelect,FileInput,TextInput,DateInput,TimeInput,EmailInput,Select,NumberInput
from django import forms
from .models import *
from .choices import SEXO
from django.forms.models import inlineformset_factory
class ModelFormFileField(ModelForm):

    class Meta:
       model = Documentos
       exclude = ['']

class ClienteForm(ModelForm):
    sexo = forms.ChoiceField(
        label='Sexo', choices=SEXO, initial='M', widget=forms.RadioSelect)

    class Meta:
        model = Cliente
        exclude = ['usuario']

        widgets = {
            'nome': TextInput(attrs={'class': 'form-control', 'placeholder': ' Nome Completo'}),
            'cpf': TextInput(attrs={'class': ' form-control'}),
            'apelido': TextInput(attrs={'class': 'form-control', 'placeholder': ' Digite um Apelido'}),
            'nascimento': DateInput(attrs={'class': 'form-control','data-language': 'pt','placeholder':'dd/mm/aaaa'}),
            'sexo': Select(attrs={'class': 'form-control'}),
            'cep': TextInput(attrs={'class': ' form-control'}),
            'email': EmailInput(attrs={'class': 'form-control','placeholder':'Example@gmail.com'}),
            'rua': TextInput(attrs={'class': 'form-control'}),
            'criado_em': DateInput(attrs={'class': 'form-control','data-language': 'pt'}),
            'atualizado_em': DateInput(attrs={'class': 'form-control'}),
            'bairro': TextInput(attrs={'class': 'form-control', 'placeholder': ' Ex: Bairro Piaui'}),
            'complemento': TextInput(attrs={'class': 'form-control', 'placeholder': ' Prox,Farmacia'}),
            'uf': Select(attrs={'class': 'form-control'}),
            'numero1': TextInput(attrs={'class': 'form-control'}),
            'numero2': TextInput(attrs={'class': 'form-control'}),
        }


class TrabalhistaForm(ModelForm):
    class Meta:
        model = Trabalhista
        exclude = ['']


widgets = {
    'ctps':TextInput(attrs={'class':'form-control','placeholder':' Carteira de Trabalho e Previdência Social'}),
    'email':EmailInput(attrs={'class':'form-control'}),
    'rua':TextInput(attrs={'class':'form-control'}),
    'admissao':DateInput(attrs={'class':'form-control','placeholder':' Ex, dd/mm/aaaa','data-language': 'pt'}),
    'demissao':DateInput(attrs={'class':'form-control','placeholder':' Ex, dd/mm/aaaa','data-language': 'pt'}),
    'recisao':DateInput(attrs={'class':'form-control','placeholder':' Ex, dd/mm/aaaa','data-language': 'pt'}),
    'salario':TextInput(attrs={'class':'form-control','placeholder':' R$ 0,00'}),
    'funcao':TextInput(attrs={'class':'form-control','placeholder':' Ex, Técnico'}),
    'entrada_manha':TimeInput(attrs={'class':'form-control','placeholder':' Digite Em Horas ,Ex 12:15'}),
    'saida_manha':TimeInput(attrs={'class':'form-control','placeholder':' Digite Em Horas ,Ex 12:15'}),
    'entrada_tarde':TimeInput(attrs={'class':'form-control','placeholder':' Digite Em Horas ,Ex 12:15'}),
    'saida_tarde':TimeInput(attrs={'class':'form-control','placeholder':' Digite Em Horas ,Ex 12:15'}),
    'obs_semana':TextInput(attrs={'class':'form-control','placeholder':' Digite Alguma Observação'}),
    'ponto':Select(attrs={'class':'form-control'}),
    'obs_ponto':TextInput(attrs={'class':'form-control','placeholder':' Digite Alguma Observação'}),
    'pergunta1':TextInput(attrs={'class':'form-control'}),

    }

TrabalhistaInline = inlineformset_factory(Cliente, Trabalhista, fields='__all__', can_delete=False, max_num=1, widgets=widgets)
docI = inlineformset_factory(Cliente, Documentos,extra=0,form=ModelFormFileField, can_delete=False, widgets=widgets)

