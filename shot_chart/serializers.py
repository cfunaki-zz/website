from rest_framework import serializers
from .models import Team, Player, Shot

class ShotSerializer(serializers.ModelSerializer):
	class Meta:
		model = Shot
		fields = ('shot_id', 'game_id', 'year', 'player', 'team', 'opp_team',
			'period', 'minutes', 'seconds', 'distance', 'x_loc', 'y_loc',
			'ppb', 'made', 'region')

class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = ('player_id', 'player_name')
