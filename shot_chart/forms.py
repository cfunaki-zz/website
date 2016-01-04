from django import forms

from .models import Team, Player


class TeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('team_id', 'team_name')

class PlayerForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = ('player_id', 'player_name')