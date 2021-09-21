from django.contrib import admin
from .models import Processo, Partes, Movimento, Distribuicao

# Register your models here.

admin.site.register(Processo)
admin.site.register(Partes)
admin.site.register(Movimento)
admin.site.register(Distribuicao)
