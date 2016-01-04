from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Team, Player, Shot
from .forms import TeamForm, PlayerForm
from .serializers import PlayerSerializer, ShotSerializer


def shot_chart(request):
	#team = get_object_or_404(Team, pk=team_id)
	player_list = Player.objects.all().order_by('player_name')
	team_list = Team.objects.all().order_by('team_name')
	query = {
		"player_list": player_list,
		"team_list": team_list,
		#"team_id": team_id
	}
	if 'player' and 'season' in request.GET:
		try:
			player_choice = request.GET['player']
			player = Player.objects.filter(player_name=player_choice)
			query_id = player[0].player_id
			query_name = player[0].player_name
			season = request.GET['season']
			query_type = "player"
			query = {
				"query_type": query_type,
				"query_id": query_id,
				"query_name": query_name,
				"season": season,
				"player_list": player_list,
				"team_list": team_list
			}
			return render(request, 'shot_chart/shotchart.html', {'query': query})
		except: pass
	if 'team' and 'season' in request.GET:
		team_choice = request.GET['team']
		team = Team.objects.filter(team_name=team_choice)
		query_id = team[0].team_id
		query_name = team[0].team_name
		season = request.GET['season']
		query_type = "team"
		query = {
			"query_type": query_type,
			"query_id": query_id,
			"query_name": query_name,
			"season": season,
			"player_list": player_list,
			"team_list": team_list
		}
		return render(request, 'shot_chart/shotchart.html', {'query': query})
	return render(request, 'shot_chart/shotchart.html', {'query': query})

@api_view(['GET'])
def team_regions(request, team_id, season):
	if request.method == 'GET':
		region_stats = Shot.team_regions(team_id, season)
		return HttpResponse(json.dumps(region_stats), content_type='application/javascript; charset=utf8')

@api_view(['GET'])
def player_regions(request, player_id, season):
	if request.method == 'GET':
		region_stats = Shot.player_regions(player_id, season)
		return HttpResponse(json.dumps(region_stats), content_type='application/javascript; charset=utf8')

@api_view(['GET'])
def shots_filter_player_season(request, player_id, season):
	if request.method == 'GET':
		if season == '0':
			shots = Shot.objects.filter(player=player_id)
		else:
			shots = Shot.objects.filter(player=player_id).filter(year=season)
		serializer = ShotSerializer(shots, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def shots_filter_team_season(request, team_id, season):
	if request.method == 'GET':
		if season == '0':
			shots = Shot.objects.filter(team=team_id)
		else:
			shots = Shot.objects.filter(team=team_id).filter(year=season)
		serializer = ShotSerializer(shots, many=True)
		return Response(serializer.data)