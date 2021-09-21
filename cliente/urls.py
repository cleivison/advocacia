from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^cliente/lista/$', views.lista),
    url(r'^cliente/$', views.listar),
    url(r'^cliente/add/$', views.add),
    url(r'^cliente/add/(?P<pk>\d+)/$', views.add, name="add"),
    url(r'^cliente/deletar/(?P<pk>\d+)/$', views.deletar,name="deletar"),
    url(r'^cliente/detalhes/(?P<pk>\d+)/$', views.detalhes,name="detalhes"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
