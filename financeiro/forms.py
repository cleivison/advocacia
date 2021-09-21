from django.forms import *
from .models import Conta_receber
from .models import Conta_pagar
from .models import Parcela
from .models import Categoria


class Conta_receberForm(ModelForm):

    class Meta:
        model = Conta_receber
        exclude = ['valor_parcela','categoria']
        widgets = {
                'descricao': TextInput(attrs={'class': 'form-control'}),
                'vencimento': DateInput(attrs={'class': 'form-control','placeholder':'dd/mm/aaaa','data-language': 'pt'}),
                'valor_total': TextInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
                'n_parcela': Select(attrs={'class':'form-control'}),
                'status_pag':CheckboxInput,
                'conta_fixa':NullBooleanSelect(attrs={'class':'form-control'}),
                'forma_pagamento':Select(attrs={'class':'form-control'}),
                'observacao':Textarea(attrs={'class':'form-control','rows':5}),
                'valor_entrada': TextInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            }


class Conta_pagarForm(ModelForm):

    class Meta:
        model = Conta_pagar
        exclude = ['id_conta','valor_parcela']
        widgets = {
                'descricao': TextInput(attrs={'class': 'form-control'}),
                'vencimento': DateInput(attrs={'class': 'form-control','placeholder':'dd/mm/aaaa','data-language': 'pt'}),
                'valor_total': TextInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
                'n_parcela': Select(attrs={'class':'form-control'}),
                'status_pag':CheckboxInput,
                'conta_fixa':NullBooleanSelect(attrs={'class':'form-control'}),
                'forma_pagamento':Select(attrs={'class':'form-control'}),
                'observacao':Textarea(attrs={'class':'form-control','rows':5}),
                'valor_entrada': TextInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
                'categoria':Select(attrs={'class':'form-control'}),
            }


class CategoriaForm(ModelForm):

    class Meta:
        model = Categoria
        exclude = ['']

        widgets = {
            'desc': TextInput(attrs={'class': 'form-control','name':'desc'})
        }

class ParcelaForm(ModelForm):

    class Meta:
        model = Parcela
        exclude = ['']
