import pandas as pd
import json
import requests
import csv
import time

directory = 'C:/Users/Chris/Documents/shot_data/'
readFile = directory + 'shots_all.csv'

shots = pd.read_csv(readFile)


players = list(shots['PLAYER_ID'].unique())
seasons = list(shots['SEASON'].unique())

playerFile = directory + 'players_agg.csv'


writeFile = open(playerFile, 'wb')

t1 = time.time()

#teamFileStr = ""
count = 0

for player_id in players:
    for season in seasons:
        shotFilterSeason = shots[shots['SEASON'] == season]
        shotFilterPlayer = shotFilterSeason[shotFilterSeason['PLAYER_ID'] == player_id]
        
        if (len(shotFilterPlayer.index) > 100):
            avgPlayerRegion = shotFilterPlayer.groupby('REGION')['MADE'].mean()
            avgAllRegion = shotFilterSeason.groupby('REGION')['MADE'].mean()
            
            regions = list(shotFilterPlayer['REGION'].unique())
            regionDict = {}
            for region in range(1, 11, 1):
                try:
                    regionDict[str(region)] = [avgPlayerRegion[region], avgAllRegion[region]]
                except:
                    regionDict[str(region)] = [0.0, avgAllRegion[region]]
                                
            shotDict = []
            
            for i, shot in shotFilterPlayer.iterrows():
                shotDict.append({'x':shot['LOC_X'],
                                 'y':shot['LOC_Y'],
                                 'made':shot['MADE'],
                                 'region':shot['REGION']})
                                     
            allData = {'regions': regionDict,
                       'shots': shotDict}
            
            dataStr = json.dumps(allData)
            strRow = str(player_id) + '|' + season + '|' + dataStr + '\n'
            
            writeFile.write(strRow)
            count +=1
            print count, player_id
            
        
t2 = time.time()

print (t2 - t1)


writeFile.close();

