import requests
import pandas as pd
import json
import urllib2


def parse_matchup(shot):
    if shot.LOCATION == 'H':
        return shot.MATCHUP[-11:-8]
    else:
        return shot.MATCHUP[-9:-6]

def get_opp_team(shot, team1, team2):
    if shot.TEAM_NAME == team1:
        return team2
    else:
        return team1
        
def get_ppb(shot):
    if shot.SHOT_TYPE == '3PT Field Goal':
        return 3
    else:
        return 2

def fix_teams(shot):
    if shot.TEAM_NAME == 'New Orleans Hornets':
        return 'New Orleans Pelicans'
    elif shot.TEAM_NAME == 'New Jersey Nets':
        return 'Brooklyn Nets'
    elif shot.TEAM_NAME == 'Seattle SuperSonics':
        return 'Oklahoma City Thunder'
    elif shot.TEAM_NAME == 'Charlotte Bobcats':
        return 'Charlotte Hornets'
    else:
        return shot.TEAM_NAME
        
def fix_opp_teams(shot):
    if shot.OPP_TEAM == 'New Orleans Hornets':
        return 'New Orleans Pelicans'
    elif shot.OPP_TEAM == 'New Jersey Nets':
        return 'Brooklyn Nets'
    elif shot.OPP_TEAM == 'Seattle SuperSonics':
        return 'Oklahoma City Thunder'
    elif shot.OPP_TEAM == 'Charlotte Bobcats':
        return 'Charlotte Hornets'
    else:
        return shot.OPP_TEAM
        
def unique_players(shot, player_list):
    p = [int(shot.PLAYER_ID), shot.PLAYER_NAME]
    if p not in player_list:
        player_list.append(p)
        
def get_region(x, y):
    # 0.3971 .9806 2.3812 0.73815
    s1 = 0.3971
    s2 = 0.95
    s3 = 2.35
    s4 = 0.59
    
    region = -1
    # inside
    if (x >= -80) and (x <= 80) and (y <= 140 + s4*x) and (y <= 140 - s4*x):
        region = 1
    # baseline right
    if (x < -80) and (x >= -220) and (y < -s2*x) and (x**2 + y**2 <= 237.5**2):
        region = 2
    # midrange right
    if (x <= 0) and (y >= -s2*x) and (y > 140 + s4*x) and (x**2 + y**2 <= 237.5**2):
        region = 3
    # midrange left
    if (x > 0) and (y >= s2*x) and (y > 140 - s4*x) and (x**2 + y**2 <= 237.5**2):
        region = 4
    # baseline left
    if (x > 80) and (x <= 220) and (y < s2*x) and (x**2 + y**2 <= 237.5**2):
        region = 5
    # right corner
    if (x < -220) and (y < -s1*x):
        region = 6
    # outside right
    if (y >= -s1*x) and (y < -s3*x) and (x**2 + y**2 > 237.5**2):
        region = 7
    # outside middle
    if (y >= -s3*x) and (y >= s3*x) and (x**2 + y**2 > 237.5**2):
        region = 8
    # outside left
    if (y >= s1*x) and (y < s3*x) and (x**2 + y**2 > 237.5**2):
        region = 9
    # left corner
    if (x > 220) and (y < s1*x):
        region = 10
    return region


def scrape_players(year):
    years = [year]
    for year in years:
        all_shots = pd.DataFrame()
        season = str(year - 1) + "-" + str(year)[2:]
        
        players_url = 'http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=%s' % (season)
        response1 = requests.get(players_url)

        headers1 = response1.json()['resultSets'][0]['headers']
        all_players = response1.json()['resultSets'][0]['rowSet']

        all_players = pd.DataFrame(all_players, columns=headers1)
        all_players = all_players[all_players['ROSTERSTATUS']==1]
        players = pd.DataFrame()
        players['PLAYER_ID'] = all_players['PERSON_ID']
        players['PLAYER_NAME'] = all_players['DISPLAY_LAST_COMMA_FIRST']
        
        i = 0
        for player_id in players['PLAYER_ID']:
            player_name = players['PLAYER_NAME'][players['PLAYER_ID']==player_id].item()
            print player_name
            player_id = str(player_id)
            player_shot_url = 'http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID=%s&Season=%s&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=' % (player_id, season)
            
            response = requests.get(player_shot_url)
            headers = response.json()['resultSets'][0]['headers']
            shots = response.json()['resultSets'][0]['rowSet']
            
            shots = pd.DataFrame(shots, columns=headers)
            shots['PLAYER_NAME'] = player_name
            
            if (i == 0):
                all_shots = shots
            else:
                all_shots = all_shots.append(shots)
            i += 1
            
        all_shots['SEASON'] = season
        all_shots['TEAM_ABB'] = all_shots.apply(lambda shot: parse_matchup(shot), axis=1)
        all_shots['OPP_TEAM_ABB'] = all_shots.apply(lambda shot: shot.MATCHUP[-3:], axis=1)
        all_shots['DATE'] = all_shots.apply(lambda shot: shot.MATCHUP[:12], axis=1)
        
        return all_shots


def scrape_games(year):
    all_shots = pd.DataFrame()
    years = [year]
    matchups = []
    fail_games = []
    count = 0
    for year in years:
        season = str(year - 1) + "-" + str(year)[2:]
        
        for game in range(1, 900, 1):
            game_id = "002" + "%s" % (season[2:4]) + "%05d" % (game)
            games_url = 'http://stats.nba.com/stats/shotchartdetail?Season=%s&SeasonType=Regular%%20Season&TeamID=0&PlayerID=0&GameID=%s&Outcome=&Location=&Month=0&SeasonSegment=&DateFrom=&Dateto=&OpponentTeamID=0&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=0&ContextMeasure=FGA' % (season, game_id)
            
            
            shots = 0
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
            response = requests.get(games_url, headers=headers)
            try:
                headers = response.json()['resultSets'][0]['headers']
                shots = response.json()['resultSets'][0]['rowSet']
                shots = pd.DataFrame(shots, columns=headers)
                    
            except:
                print 'Fail:', game
                fail_games.append(game)
                continue
            
            try:
                matchups = list(shots.TEAM_NAME.unique())
                shots['OPP_TEAM'] = shots.apply(lambda shot: get_opp_team(shot, matchups[0], matchups[1]), axis=1)
                shots['PPB'] = shots.apply(lambda shot: get_ppb(shot), axis=1)
                shots['REGION'] = shots.apply(lambda shot: get_region(shot.LOC_X, shot.LOC_Y), axis=1)
                shots['MADE'] = shots['SHOT_MADE_FLAG']
                all_shots = all_shots.append(shots)
                print game
            except:
                pass
        
    all_shots['SEASON'] = season
    all_shots['INDEX'] = all_shots.index + 1
    all_shots = all_shots.drop(['GRID_TYPE',
                                'GAME_EVENT_ID',
                                'EVENT_TYPE',
                                'ACTION_TYPE',
                                'SHOT_TYPE',
                                'SHOT_ZONE_BASIC',
                                'SHOT_ZONE_AREA',
                                'SHOT_ZONE_RANGE',
                                'SHOT_MADE_FLAG',
                                'SHOT_ATTEMPTED_FLAG'],
                                axis=1)
    
    
    all_shots = all_shots[['GAME_ID',
                           'PLAYER_ID',
                           'PLAYER_NAME',
                           'TEAM_ID',
                           'TEAM_NAME',
                           'PERIOD',
                           'MINUTES_REMAINING',
                           'SECONDS_REMAINING',
                           'SHOT_DISTANCE',
                           'LOC_X',
                           'LOC_Y',
                           'OPP_TEAM',
                           'PPB',
                           'REGION',
                           'MADE',
                           'SEASON',
                           'INDEX'
                           ]]
            
    return all_shots

def player_data(shots, directory):
    player_list = []
    shots.apply(lambda shot: unique_players(shot, player_list), axis=1)  
    player_df = pd.DataFrame(player_list, columns=['PLAYER_ID','PLAYER_NAME'])
    player_df = player_df.sort_values('PLAYER_NAME')
    
    file_name = directory + "players.csv"
    player_df.to_csv(file_name, index=False)
    return player_df
    
def team_data(shots, directory):
    shots['TEAM_NAME'] = shots.apply(lambda shot: fix_teams(shot), axis=1)
    name_list = list(shots.TEAM_NAME.unique())
    id_list = list(shots.TEAM_ID.unique())
    teams = pd.DataFrame(id_list, columns=['TEAM_ID'])
    teams['TEAM_NAME'] = name_list
    teams = teams.sort_values('TEAM_NAME')
    
    file_name = directory + "teams.csv"
    teams.to_csv(file_name, index=False)
    return teams

def save_shots(directory, season, shots):
    file_name = directory + "shots_" + "%s" %(season) + ".csv"
    print file_name
    shots.to_csv(file_name, index=False)

# Get shot data from given range of seasons and append into single data frame
def load_shots(directory):
    all_shots = pd.DataFrame()
    for season in range(2013, 2017, 1):
        print season
        file_name = directory + "shots_%s.csv" % (season)
        shots = pd.read_csv(file_name)
        all_shots = all_shots.append(shots)
    return all_shots

def fix_opp_team(shots, teams):
    def into_dict(team, team_dict):
        team_dict[team.TEAM_NAME] = int(team.TEAM_ID)
    def get_team_id(shot, team_dict):
        opp_team_id = team_dict[shot.OPP_TEAM]
        return opp_team_id
    team_dict = {}
    teams.apply(lambda team: into_dict(team, team_dict), axis=1)
    shots['OPP_TEAM'] = shots.apply(lambda shot: fix_opp_teams(shot), axis=1)
    shots['OPP_TEAM_ID'] = shots.apply(lambda shot: get_team_id(shot, team_dict), axis=1)

def clean_shots(shots, directory):
    del shots['PLAYER_NAME']
    del shots['TEAM_NAME']
    del shots['OPP_TEAM']
    shots['OPP_TEAM'] = shots['OPP_TEAM_ID']
    del shots['OPP_TEAM_ID']
    del shots['INDEX']
    shots['INDEX'] = shots.index + 1
    
    file_name = directory + "shots_all.csv"
    shots.to_csv(file_name, index=False) 
    
def combine_season_files(directory):
    shots_all = load_shots(directory)
    players = player_data(shots, directory)
    teams = team_data(shots, directory)
    fix_opp_team(shots, teams)
    clean_shots(shots, directory)
    save_shots(directory, "all", shots)
    return shots_all

# Choose directory to store csv files
directory = "C:/Users/Chris/Documents/shot_data/"
# Choose season. 2016 = 2015-16 season
season = 2016

# Scrapes shot log of every player in a given season
#shots = scrape_players(season)

# Scrapes shot log of every game in a given regular season
#shots = scrape_games(season)
#save_shots(directory, season, shots)
shots_all = combine_season_files(directory)