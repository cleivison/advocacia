from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^processo_trabalhista/add/$', views.add),
    url(r'^processo_trabalhista/$', views.home),
    url(r'^processo_trabalhista/lista/$', views.lista)
]
