from django.forms import *
from .models import *

class funcionarioForm(ModelForm):

    class Meta:
        model = funcionario
        exclude = ['user']
        widgets = {
                'perfil': Select(attrs={'class':'form-control'}),
            }