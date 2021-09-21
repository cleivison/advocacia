from django.conf.urls import include, url
from . import views
import os
import requests
urlpatterns = [
	url(r'^pdf/(?P<pk>\d+)/$',views.open_pdf),
    url(r'^diario/$',views.listar),
    url(r'^diario/buscar/$', views.busca_diario),
    url(r'^diario/deletar/(?P<pk>\d+)/$', views.deletar_diario),
    url(r'^diario/trt22/$', views.trt22),
]
