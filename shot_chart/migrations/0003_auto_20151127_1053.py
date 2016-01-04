# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shot_chart', '0002_auto_20151126_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shot',
            name='opp_team_id',
        ),
        migrations.RemoveField(
            model_name='shot',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='shot',
            name='team_id',
        ),
        migrations.AddField(
            model_name='shot',
            name='opp_team',
            field=models.ForeignKey(to='shot_chart.Team', related_name='opp_team', null=True),
        ),
        migrations.AddField(
            model_name='shot',
            name='player',
            field=models.ForeignKey(to='shot_chart.Player', null=True),
        ),
        migrations.AddField(
            model_name='shot',
            name='team',
            field=models.ForeignKey(to='shot_chart.Team', related_name='team', null=True),
        ),
    ]
