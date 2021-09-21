from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^processo/add/$', views.add),
    url(r'^processo/$', views.processo_lista),
    url(r'^processo/(?P<pk>\d+)/$', views.processos_detalhes),
    url(r'^processo/atualizar/(?P<pk>\d+)/$', views.processos_atualizar),
    url(r'^processo/deletar/(?P<pk>\d+)/$', views.deletar_processo),
]
