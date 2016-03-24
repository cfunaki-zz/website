from django.shortcuts import render
from django.core import serializers
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework.response import Response


def crime_map(request):
	return render(request, 'crime_map.html')

@api_view(['GET'])
def get_zipcodes(request):
	string = 'zipcode'
	cursor = connection.cursor()
	cursor.execute("SELECT agg_data FROM crime_zip WHERE type = 'zipcode'")
	data = cursor.fetchone()
	"""
	data = [{'latitude': 34.0, 'longitude': -118.3, 'type': 'homicide'}, \
			{'latitude': 33.9, 'longitude': -118.2, 'type': 'theft'}]
	"""
	return Response(data)

@api_view(['GET'])
def get_crimes(request):
	string = 'crime'
	cursor = connection.cursor()
	cursor.execute("SELECT agg_data FROM crime_zip WHERE type = 'crime'")
	data = cursor.fetchone()
	return Response(data)