# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shot_chart', '0004_auto_20151129_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerAgg',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('player_year_agg', models.CharField(max_length=50)),
                ('player_region_agg', models.TextField()),
                ('player_shots_agg', models.TextField()),
                ('player_agg', models.ForeignKey(null=True, to='shot_chart.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamAgg',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('team_year_agg', models.CharField(max_length=50)),
                ('team_region_agg', models.TextField()),
                ('team_shots_agg', models.TextField()),
                ('team_agg', models.ForeignKey(null=True, to='shot_chart.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='shot',
            old_name='clock',
            new_name='seconds',
        ),
        migrations.RemoveField(
            model_name='shot',
            name='x_bin',
        ),
        migrations.RemoveField(
            model_name='shot',
            name='y_bin',
        ),
        migrations.AddField(
            model_name='shot',
            name='distance',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shot',
            name='game_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shot',
            name='minutes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shot',
            name='year',
            field=models.CharField(max_length=50),
        ),
    ]
