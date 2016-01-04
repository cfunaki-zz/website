# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.IntegerField(serialize=False, primary_key=True)),
                ('player_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('shot_id', models.IntegerField(serialize=False, primary_key=True)),
                ('year', models.IntegerField()),
                ('made', models.IntegerField()),
                ('period', models.IntegerField()),
                ('clock', models.IntegerField()),
                ('x_loc', models.IntegerField()),
                ('y_loc', models.IntegerField()),
                ('ppb', models.IntegerField()),
                ('x_bin', models.FloatField()),
                ('y_bin', models.FloatField()),
                ('region', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.IntegerField(serialize=False, primary_key=True)),
                ('team_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='shot',
            name='opp_team_id',
            field=models.ForeignKey(to='shot_chart.Team', related_name='shot_opp_team_id'),
        ),
        migrations.AddField(
            model_name='shot',
            name='player_id',
            field=models.ForeignKey(to='shot_chart.Player', related_name='shot_player_id'),
        ),
        migrations.AddField(
            model_name='shot',
            name='team_id',
            field=models.ForeignKey(to='shot_chart.Team', related_name='shot_team_id'),
        ),
    ]
