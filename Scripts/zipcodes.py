import os
import csv
import pandas as pd

directory = os.path.dirname(os.path.realpath(__file__))

def filter_zip():
    fileName = os.path.join(directory, 'zipcode_nodup.csv')
    writeFile = directory + '\zipcode_nodup_ca.csv'
    zips = pd.read_csv(fileName)
    zips = zips[zips['state'] == 'CA']
    zips = zips[zips['longitude'] < -115]
    zips = zips[zips['longitude'] > -122]
    
    zips = zips[zips['latitude'] < 37]
    zips = zips[zips['latitude'] > 31]
    
    zips['ZIP']  = zips.zip.astype(str)
    zips['LATITUDE'] = zips.latitude
    zips['LONGITUDE'] = zips.longitude
    columns = ['ZIP', 'LATITUDE', 'LONGITUDE']
    
    zips = zips[columns]
    
    zips.to_csv(writeFile, index=False)
    
#filter_zip()

crimeFile = directory + '\crime_filtered_clean.csv'
zipFile = directory + '\zipcode_nodup_ca.csv'

crime = pd.read_csv(crimeFile)
zips = pd.read_csv(zipFile)

def fix_zip(zipcode):
    return str(zipcode)[:5]

crime['ZIP'] = crime.apply(lambda row: fix_zip(row['ZIP']), axis=1)
zips['ZIP'] = zips.apply(lambda row: fix_zip(row['ZIP']), axis=1)

zips.index = zips['ZIP']


homicides = crime.groupby('ZIP')['HOMICIDE'].sum()
thefts = crime.groupby('ZIP')['THEFT'].sum()
violent = crime.groupby('ZIP')['VIOLENT'].sum()
gang = crime.groupby('ZIP')['GANG'].sum()

result = pd.concat([zips, homicides, thefts, violent, gang], axis=1)

result = result.dropna(subset=['ZIP'], how='all')
result = result.fillna(0)

result['HOMICIDE'] = result['HOMICIDE'].astype(int)
result['THEFT'] = result['THEFT'].astype(int)
result['VIOLENT'] = result['VIOLENT'].astype(int)
result['GANG'] = result['GANG'].astype(int)

writeFile = directory + '\zipcode_clean.csv'
result.to_csv(writeFile, index=False)