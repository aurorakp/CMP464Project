# Aurora Koch-Pongsema
# CMP 464: Spring 2016
# Project: Data Collection
# Grand Theft Auto Data Set

import math, csv, re, sys
from datetime import datetime as dt

# Data downloaded as of 4/17/2016 

data_file = "NYPD_GTA_2015.csv"

thefts = {}

# Note: I have to label each theft by Object ID as it appears that most thefts
# are listed by the half hour, or at least by round numbers for minutes, meaning
# that if I classify it by the time, I will get duplicate entries.  The possibility
# for duplicate entries also exists for location.

with open(data_file,'rU') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        try:
            if row['Location 1'] != '':
                objectID = row['OBJECTID']
                dtstring = row['Occurrence Date']
                date_time = dt.strptime(dtstring, '%m/%d/%Y %I:%M:%S %p')
                sector = row['Sector']
                precinct = row['Precinct']
                borough = row['Borough']
                loc = (re.sub(r'[\(\,\)]','',row['Location 1'])).split(" ")
                lat = float(loc[0])
                lon = float(loc[1])
                thefts[objectID] = (date_time, lat, lon, sector, precinct, borough)

        except:
            print 'objectid is: ' + objectID
            print 'row is: '
            print row.items()
            print sys.exc_traceback.tb_lineno


print "Total incidents: " + str(len(thefts))
vals = thefts.values()

bxvals = len([vals[v] for v in range(len(thefts)) if vals[v][5] == 'BRONX'])
bkvals = len([vals[v] for v in range(len(thefts)) if vals[v][5] == 'BROOKLYN'])
qvals = len([vals[v] for v in range(len(thefts)) if vals[v][5] == 'QUEENS'])
mvals = len([vals[v] for v in range(len(thefts)) if vals[v][5] == 'MANHATTAN'])
sivals = len([vals[v] for v in range(len(thefts)) if vals[v][5] == 'STATEN ISLAND'])

print "Incidents in the Bronx: " + str(bxvals)
print "Incidents in Brooklyn: " + str(bkvals)
print "Incidents in Queens: " + str(qvals)
print "Incidents in Manhattan: " + str(mvals)
print "Incidents in Staten Island: " + str(sivals)

print "Total (are any missing?) " + str(bxvals + bkvals + qvals + mvals + sivals)
                
                
        
