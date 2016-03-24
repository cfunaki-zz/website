import pandas as pd
import json

# crime_filter.py
# zipcodes.py
# zip_crime_to_json.py

directory = os.path.dirname(os.path.realpath(__file__))

zipFile = directory + '\zipcode_clean.csv'
crimeFile = directory + '\crime_filtered_clean.csv'

zips = pd.read_csv(zipFile)
crime = pd.read_csv(crimeFile)


crimeDict = []

def crime_json():
    for i, row in crime.iterrows():
        crimeDict.append({#'zip': str(int(row['ZIP'])),
                          'latitude': row['LATITUDE'],
                          'longitude': row['LONGITUDE'],
                          'homicide': int(row['HOMICIDE']),
                          'theft': int(row['THEFT']),
                          'violent': int(row['VIOLENT']),
                          'gang': int(row['GANG']),
                          })

zipDict = []

def zip_json():
    for i, row in zips.iterrows():
        zipDict.append({'zip': str(int(row['ZIP'])),
                        'latitude': row['LATITUDE'],
                        'longitude': row['LONGITUDE'],
                        'homicide': int(row['HOMICIDE']),
                        'theft': int(row['THEFT']),
                        'violent': int(row['VIOLENT']),
                        'gang': int(row['GANG']),
                        })
                    
crime_json()
zip_json()

crimeStr = 'crime|' + json.dumps(crimeDict) + '\n'
zipStr = 'zipcode|' + json.dumps(zipDict) + '\n'

crimeZipFile = directory + '\crime_zip.csv'
crimeZipWriteFile = open(crimeZipFile, 'wb')

crimeZipWriteFile.write(crimeStr)
crimeZipWriteFile.write(zipStr)

crimeZipWriteFile.close()




