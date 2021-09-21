from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^usuario/registro/$', views.registro_usuario),
    url(r'^usuario/login/$', views.login_usuario),
    url(r'^usuario/$', views.lista_usuario),
    url(r'^usuario/excluir/(?P<username>[\w|\W.-]+)/$', views.deletar_usuario),
    url(r'^usuario/logout/$', views.logout_usuario),
    url(r'^usuario/error/$', views.error_usuario),
    url(r'^usuario/recuperar/$', views.recuperar_senha),
    url(r'^usuario/senha/$', views.mudar_senha),
]
