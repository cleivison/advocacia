# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	url(r'^$', views.site),
	url(r'sobre/$', views.sobre),
	url(r'servicos/$', views.servicos),
	url(r'contato/$', views.contato),
]