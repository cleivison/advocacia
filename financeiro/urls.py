# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^contas/add_pagar/$', views.contaPagar),
    url(r'^contas/pagar/$', views.contas_pagar_lista),
    #url(r'^contas/$', views.contas),
    url(r'^contas/pagar/(?P<pk>\d+)/$', views.conta_detalhada_pagar),
    url(r'^contas/pagar/deletar/(?P<pk>\d+)/$', views.deletar_pagar),
    url(r'^contas/pagar/atualizar/(?P<pk>\d+)/$', views.atualizar_conta_pagar),
    url(r'^contas/pagar/aberta/$', views.conta_pagar_aberta),
    url(r'^contas/pagar/pagas/$', views.conta_apagar_pagas),
    url(r'^contas/pagar/fixas/$', views.contas_fixas),
    url(r'^add/categoria/$', views.add_categoria,name="categoria"),
    ###grafico
    url(r'^contas/pagar/receitas/$', views.receitas),

    url(r'^contas/add_receber/$', views.contaReceber),
    url(r'^contas/add_receber/(?P<pk>\d+)/$', views.contaReceber),
    url(r'^contas/receber/$', views.contas_receber_lista),
    url(r'^contas/receber/(?P<pk>\d+)/$', views.conta_detalhada_receber),
    url(r'^contas/receber/deletar/(?P<pk>\d+)/$', views.deletar_receber),
    url(r'^contas/receber/atualizar/(?P<pk>\d+)/$', views.atualizar_conta_receber),
    url(r'^contas/receber/aberta/$', views.conta_receber_aberta),
    url(r'^contas/receber/pagas/$', views.conta_receber_pagas),
    url(r'^contas/parcela/(?P<pk>\d+)/$', views.pagar_parcela),
]
