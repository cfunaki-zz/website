from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.blog, name='blog'),
	url(r'^shooting_efficiency/$', views.post1, name='post1'),
	url(r'^sampling_macro/$', views.post2, name='post2'),
	url(r'^shot_charts/$', views.post3, name='post3'),
	#url(r'^$', views.post_list, name='post_list'),
	#url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
	#url(r'^post/new/$', views.post_new, name='post_new'),
	#url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
]