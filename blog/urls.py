from django.conf.urls import include, url
from django.views.generic import TemplateView
from blog.views import *
from . import views

urlpatterns = [
    url(r'^blog/$', views.post_list),
    url(r'^blog/all/posts/$', views.list),
    url(r'^blog/post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^blog/post/novo/$', views.post_new, name='post_new'),
    url(r'^blog/nova/tag/$', views.new_tag, name='new_tag'),
    url(r'^blog/post/(?P<pk>[0-9]+)/editar/$', views.post_edit, name='post_edit'),
    url(r'^blog/deletar/post(?P<pk>\d+)/$', views.excluir_post,name='excluir_post'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', TagPostsView.as_view(), name='tag_posts_page'),
]