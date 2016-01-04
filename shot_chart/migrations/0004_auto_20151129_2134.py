# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shot_chart', '0003_auto_20151127_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='opp_team',
            field=models.ForeignKey(related_name='opp_team_set', to='shot_chart.Team', null=True),
        ),
        migrations.AlterField(
            model_name='shot',
            name='team',
            field=models.ForeignKey(related_name='team_set', to='shot_chart.Team', null=True),
        ),
    ]
