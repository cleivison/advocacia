# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^agenda/$', views.home),
    url(r'^agenda/(?P<pk>\d+)/$', views.detalhes,name="detalhes_evento"),
    url(r'^agenda/registro_evento/$', views.novo_evento,name="novo_evento"),
    url(r'^agenda/delete/(?P<pk>\d+)/$', views.deletar,name="deletar_evento"),
    url(r'^agenda/atualizar/(?P<pk>\d+)/$', views.atualizar_contato),
]
