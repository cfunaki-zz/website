from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    url(r'^$', 'mysite.views.home', name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shotchart/', include('shot_chart.urls', namespace="shot_chart")),
    url(r'^crime/', include('crime.urls', namespace="crime")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

