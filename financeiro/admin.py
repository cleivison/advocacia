# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Conta_receber
from .models import Conta_pagar
from .models import Parcela
from .models import Categoria
# Register your models here.


class ContaApagarAdmin(admin.ModelAdmin):
    list_display = ('vencimento', 'n_parcela', 'criado_em', 'status_pag')


admin.site.register(Conta_pagar, ContaApagarAdmin)
admin.site.register(Conta_receber)
admin.site.register(Parcela)
admin.site.register(Categoria)
