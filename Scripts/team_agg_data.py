import pandas as pd
import json
import requests
import csv
import time

directory = 'C:/Users/Chris/Documents/shot_data/'
readFile = directory + 'shots_all.csv'

shots = pd.read_csv(readFile)


teams = list(shots['TEAM_ID'].unique())
players = list(shots['PLAYER_ID'].unique())
seasons = list(shots['SEASON'].unique())

teamFile = directory + 'teams_agg.csv'
playerFile = directory + 'players_agg.csv'


writeFile = open(teamFile, 'wb')

t0 = time.time()
"""
teamFileStr1 = ""
index = 1
for team_id in teams[:1]:
    print team_id
    for season in seasons[:]:
        regionsURL = "http://www.cfunaki.com/shotchart/api/team_regions/team_id=%d/season=%s/" % (team_id, season)
        shotsURL = "http://www.cfunaki.com/shotchart/api/teams/team_id=%d/season=%s/?format=json" % (team_id, season)
        
        regionsResponse = requests.get(regionsURL)
        regionsJSON = regionsResponse.json()
        regionsStr = json.dumps(regionsJSON)
        regionsStr = regionsStr.replace('"', "'")
        
        shotsResponse = requests.get(shotsURL)
        shotsJSON1 = shotsResponse.json()
        shotsJSON2 = []
        
        for shot in shotsJSON1:
            shotsJSON2.append({'x':shot['x_loc'], 'y':shot['y_loc'],'made':shot['made'],'region':shot['region']})
        
        shotsStr = json.dumps(shotsJSON2)
        
        strRow1 = str(index) + '|' + str(team_id) + '|' + season + '|' + regionsStr + '|' + shotsStr + '\n'
        teamFileStr1 += strRow1
        index +=1
"""
t1 = time.time()

#teamFileStr = ""
index = 1

for team_id in teams:
    print team_id
    for season in seasons:
        shotFilterSeason = shots[shots['SEASON'] == season]
        shotFilterTeam = shotFilterSeason[shotFilterSeason['TEAM_ID'] == team_id]
                            
        avgTeamRegion = shotFilterTeam.groupby('REGION')['MADE'].mean()
        avgAllRegion = shotFilterSeason.groupby('REGION')['MADE'].mean()
        
        regionDict = {'1': [avgTeamRegion[1], avgAllRegion[1]],
                      '2': [avgTeamRegion[2], avgAllRegion[2]],
                      '3': [avgTeamRegion[3], avgAllRegion[3]],
                      '4': [avgTeamRegion[4], avgAllRegion[4]],
                      '5': [avgTeamRegion[5], avgAllRegion[5]],
                      '6': [avgTeamRegion[6], avgAllRegion[6]],
                      '7': [avgTeamRegion[7], avgAllRegion[7]],
                      '8': [avgTeamRegion[8], avgAllRegion[8]],
                      '9': [avgTeamRegion[9], avgAllRegion[9]],
                      '10': [avgTeamRegion[10], avgAllRegion[10]]
                      }
                            
        shotDict = []
        
        for i, shot in shotFilterTeam.iterrows():
            shotDict.append({'x':shot['LOC_X'],
                             'y':shot['LOC_Y'],
                             'made':shot['MADE'],
                             'region':shot['REGION']})
                             
        allData = {'regions': regionDict,
                   'shots': shotDict}
        
        dataStr = json.dumps(allData)
        strRow = str(team_id) + '|' + season + '|' + dataStr + '\n'
        
        writeFile.write(strRow)
        index +=1
            
        
t2 = time.time()

print (t1 - t0)
print (t2 - t1)


writeFile.close();

