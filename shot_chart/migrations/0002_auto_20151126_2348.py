# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shot_chart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='opp_team_id',
            field=models.ForeignKey(to='shot_chart.Team', related_name='shot_opp_team'),
        ),
        migrations.AlterField(
            model_name='shot',
            name='player_id',
            field=models.ForeignKey(to='shot_chart.Player', related_name='shot_player'),
        ),
        migrations.AlterField(
            model_name='shot',
            name='team_id',
            field=models.ForeignKey(to='shot_chart.Team', related_name='shot_team'),
        ),
    ]
