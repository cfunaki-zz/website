from django.conf.urls import patterns, url


from . import views

urlpatterns = [
	url(r'^$', views.crime_map, name='crime'),
	url(r'^api/zipcodes/$', views.get_zipcodes, name='get_zipcodes'),
	url(r'^api/crimes/$', views.get_crimes, name='get_crimes'),
]