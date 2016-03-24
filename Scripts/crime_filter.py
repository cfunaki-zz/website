import os
import csv
import pandas as pd

directory = os.path.dirname(os.path.realpath(__file__))
readFileName = os.path.join(directory, 'V_Crime_Month.csv')
writeFileName = directory + '\crime_filtered.csv'

#data = pd.read_csv(readFileName, nrows=100)

def filter_crime_data():
    
    readFile = open(readFileName, 'r')
    reader = csv.reader(readFile)
    
    writeFile = open(writeFileName, 'wb')
    writer = csv.writer(writeFile)
    
    years = ['2010', '2011', '2012', '2013', '2014']
    
    for row in reader:
        if (row[1] == '2014' or row[1] == 'CRIME_YEAR'):
            writer.writerows([row])
            
    readFile.close()
    writeFile.close()

#filter_crime_data()

data = pd.read_csv(writeFileName)

data['HOMICIDE'] = ['homicide' in x.lower() for x in data['CRIME_CATEGORY_DESCRIPTION']]
data['THEFT'] = [('theft' in x.lower()) or \
                ('burglary' in x.lower()) or \
                ('robbery' in x.lower()) \
                for x in data['CRIME_CATEGORY_DESCRIPTION']]
data['VIOLENT'] = [x == 'Violent' for x in data['CRIME_TYPE']]
data['GANG'] = [x == 'Y' for x in data['GANG_RELATED']]

data['YEAR'] = data['CRIME_YEAR']
data['MONTH'] = data['month']
data['ID'] = data.index + 1


columns = ['ID', 'ZIP', 'LATITUDE', 'LONGITUDE', 'YEAR', 'MONTH', 'HOMICIDE', 'THEFT', 'VIOLENT', 'GANG']
data = data[columns]

data['HOMICIDE'] = data['HOMICIDE'].astype(int)
data['THEFT'] = data['THEFT'].astype(int)
data['VIOLENT'] = data['VIOLENT'].astype(int)
data['GANG'] = data['GANG'].astype(int)

writeFileNameClean = directory + '\crime_filtered_clean.csv'
data.to_csv(writeFileNameClean, index=False)
