from django.conf.urls import patterns, url

from . import views

urlpatterns = [
	url(r'^$', views.shot_chart, name='shot_chart'),
	#url(r'^teams/(?P<team_id>[0-9]+)/$', views.team_view, name='team_view'),
	url(r'^api/players/player_id=(?P<player_id>[0-9]+)/season=(?P<season>[a-z0-9_-]+)/$', views.shots_filter_player_season, name='shots_filter_player_season'),
	url(r'^api/teams/team_id=(?P<team_id>[0-9]+)/season=(?P<season>[a-z0-9_-]+)/$', views.shots_filter_team_season, name='shots_filter_team_season'),
	url(r'^api/team_regions/team_id=(?P<team_id>[0-9]+)/season=(?P<season>[a-z0-9_-]+)/$', views.team_regions, name='team_regions'),
	url(r'^api/player_regions/player_id=(?P<player_id>[0-9]+)/season=(?P<season>[a-z0-9_-]+)/$', views.player_regions, name='player_regions'),
]