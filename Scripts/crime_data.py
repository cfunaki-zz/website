import pandas as pd
import os
from dateutil.parser import parse
import datetime

readFile = 'C:\Users\Chris\Documents\LA_Crime\V_Crime_Month.csv'
writeFile = 'C:\Users\Chris\Documents\LA_Crime\crime_2015.csv'

data = pd.read_csv(readFile, nrows=100)

date = data['CRIME_DATE']

crime_desc = list(data['CRIME_CATEGORY_DESCRIPTION'].unique())

def parse_date(date):
    dateStr = date[0:2] + ' ' + date[2:5] + ' ' + date[5:7] + ' ' + date[8:]
    datetime = parse(dateStr)
    return datetime
def parse_gang(gang):
    if (gang == 'Y'):
        return True
    else:
        return False
def parse_violent(violent):
    if (violent == 'Violent'):
        return True
    else:
        return False
    
data['DATETIME'] = data.apply(lambda row: parse_date(row['CRIME_DATE']), axis=1)

data['GANG_RELATED'] = data.apply(lambda row: parse_gang(row['GANG_RELATED']), axis=1)

data['VIOLENT'] = data.apply(lambda row: parse_violent(row['CRIME_TYPE']), axis=1)


crime = data[['CRIME_IDENTIFIER', 'CRIME_CATEGORY_DESCRIPTION', 'DATETIME', 'ZIP', 'LATITUDE', 'LONGITUDE', 'VICTIM_COUNT', 'GANG_RELATED', 'VIOLENT']]

mask = crime['CRIME_CATEGORY_DESCRIPTION']

#crime.to_csv(writeFile, index=False)