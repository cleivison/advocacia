from django.forms import ModelForm,RadioSelect,TextInput,Textarea,DateInput,TimeInput,EmailInput,Select,NumberInput, NullBooleanSelect, FileInput
from django import forms
from .models import Processo, Partes, Movimento, Distribuicao
from django.forms.models import inlineformset_factory


class ProcessoForm(ModelForm):

    class Meta:
        model = Processo
        exclude = ['']

        widgets = {
            'numero_acervo': TextInput(attrs={'class': 'form-control', 'placeholder': ' Numero do Acervo'}),
            'numero_processo': TextInput(attrs={'class': 'form-control', 'placeholder': ' Numero Processo'}),
            'data_abertura': DateInput(attrs={'class': 'form-control', 'placeholder': ' dd/mm/aaaa'}),
            'comarca': TextInput(attrs={'class': 'form-control'}),
            'assistencia_judiciaria': TextInput(attrs={'class': ' form-control'}),
            'natureza': TextInput(attrs={'class': 'form-control'}),
            'classe_processual': TextInput(attrs={'class': 'form-control'}),
            'assuntos': TextInput(attrs={'class': 'form-control'}),
            'observacao': TextInput(attrs={'class': 'form-control'}),
            'valor_acao': TextInput(attrs={'class': 'form-control'}),
            'usuario':Select(attrs={'class':'form-control'}),
            'status_atual': TextInput(attrs={'class': 'form-control'}),
            'status_processo': NullBooleanSelect(attrs={'class': 'form-control'}),
        }


class PartesForm(ModelForm):
    class Meta:
        model = Partes
        exclude = ['']

        widgets = {
            'parte':TextInput(attrs={'class':'form-control'}),
            'descricao':TextInput(attrs={'class':'form-control'}),
        }


class MovimentoForm(ModelForm):
    class Meta:
        model = Movimento
        exclude = ['']

        widgets = {
            'data_movimentacao':DateInput(attrs={'class':'form-control'}),
            'descricao':TextInput(attrs={'class':'form-control'}),
            'doc':FileInput(attrs={'class':'form-control'}),
        }


class DistribuicaoForm(ModelForm):
    class Meta:
        model = Distribuicao
        exclude = ['']

widgets = {
        'realizada':DateInput(attrs={'class':'form-control'}),
        'tipo_distribuicao':TextInput(attrs={'class':'form-control'}),
        'comarca':TextInput(attrs={'class':'form-control'}),
        'secretaria':TextInput(attrs={'class':'form-control'}),
        'motivo':TextInput(attrs={'class':'form-control'}),
}

ProcessosInline = inlineformset_factory(Processo, Partes, fields='__all__', can_delete=False, max_num=1, widgets=widgets)
ProcessosInline2 = inlineformset_factory(Processo, Movimento, fields='__all__', can_delete=False, max_num=1, widgets=widgets)
ProcessosInline3 = inlineformset_factory(Processo, Distribuicao, fields='__all__', can_delete=False, max_num=1, widgets=widgets)
