from django.db import models

class Team(models.Model):
	team_id = models.IntegerField(primary_key=True)
	team_name = models.CharField(max_length=50)
	def __str__(self):
		return self.team_name

class Player(models.Model):
	player_id = models.IntegerField(primary_key=True)
	player_name = models.CharField(max_length=50)
	def __str__(self):
		return self.player_name

class Shot(models.Model):
	shot_id = models.IntegerField(primary_key=True)
	game_id = models.IntegerField()
	year = models.CharField(max_length=50)
	player = models.ForeignKey(Player, null=True)
	team = models.ForeignKey(Team, null=True, related_name='team_set')
	opp_team = models.ForeignKey(Team, null=True, related_name='opp_team_set')
	period = models.IntegerField()
	minutes = models.IntegerField()
	seconds = models.IntegerField()
	distance = models.IntegerField()
	x_loc = models.IntegerField()
	y_loc = models.IntegerField()
	ppb = models.IntegerField()
	made = models.IntegerField()
	region = models.IntegerField()

	def team_regions(team_id, season):
		from django.db.models import Avg
		region_stats = {}
		for i in range(1, 11):
			if season == '0':
				team_pct = Shot.objects.filter(team=team_id).filter(region=i).aggregate(Avg('made'))
				nba_pct = Shot.objects.filter(region=i).aggregate(Avg('made'))
			else:
				team_pct = Shot.objects.filter(team=team_id).filter(region=i).filter(year=season).aggregate(Avg('made'))
				nba_pct = Shot.objects.filter(region=i).filter(year=season).aggregate(Avg('made'))
			team_pct = team_pct['made__avg']
			nba_pct = nba_pct['made__avg']
			region_stats[i] = [team_pct, nba_pct]
		return region_stats

	def player_regions(player_id, season):
		from django.db.models import Avg
		region_stats = {}
		for i in range(1, 11):
			if season == '0':
				player_pct = Shot.objects.filter(player=player_id).filter(region=i).aggregate(Avg('made'))
				nba_pct = Shot.objects.filter(region=i).aggregate(Avg('made'))
			else:
				player_pct = Shot.objects.filter(player=player_id).filter(region=i).filter(year=season).aggregate(Avg('made'))
				nba_pct = Shot.objects.filter(region=i).filter(year=season).aggregate(Avg('made'))
			player_pct = player_pct['made__avg']
			nba_pct = nba_pct['made__avg']
			region_stats[i] = [player_pct, nba_pct]
		return region_stats