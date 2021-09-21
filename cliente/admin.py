from django.contrib import admin
from .models import Cliente,  Trabalhista,Documentos

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome','cpf','nascimento')

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('doc_name',)

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Documentos,DocumentoAdmin)
admin.site.register(Trabalhista)
