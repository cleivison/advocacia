# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Evento

# Register your models here.
class Agenda(admin.ModelAdmin):
	list_display = ['id_evento','titulo']
admin.site.register(Evento,Agenda)
