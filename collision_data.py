# Aurora Koch-Pongsema
# CMP 464: Spring 2016
# Project: Data Collection
# Collisions Data Set

import math, csv, re, sys
from datetime import datetime as dt

# Data downloaded as of 4/17/2016 - note that some potholes, etc., may be
# closed at this point that are open

data_file = "NYPD_Motor_Vehicle_Collisions_2015.csv"

colls = {}
contribs = []
colls_pavement = {}


with open(data_file,'rU') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        try:
            if row['LOCATION'] != '':
                dtstring = row['DATE'] + " " + row['TIME']
                date_time = dt.strptime(dtstring, '%m/%d/%Y %H:%M')
                lat = float(row['LATITUDE'])
                lon = float(row['LONGITUDE'])
                ctrib = ""
                

                # If there are contributing factors recorded, add them to
                # both the set, and the specific factors for the collisions
                
                if row['CONTRIBUTING FACTOR VEHICLE 1'] != '':
                    contribs.append(row['CONTRIBUTING FACTOR VEHICLE 1'])
                    ctrib += row['CONTRIBUTING FACTOR VEHICLE 1'] + ","
                if row['CONTRIBUTING FACTOR VEHICLE 2'] != '':
                    contribs.append(row['CONTRIBUTING FACTOR VEHICLE 2'])
                    ctrib += row['CONTRIBUTING FACTOR VEHICLE 2'] + ","
                if row['CONTRIBUTING FACTOR VEHICLE 3'] != '':
                    contribs.append(row['CONTRIBUTING FACTOR VEHICLE 3'])
                    ctrib += row['CONTRIBUTING FACTOR VEHICLE 3'] + "," 
                if row['CONTRIBUTING FACTOR VEHICLE 4'] != '':
                    contribs.append(row['CONTRIBUTING FACTOR VEHICLE 4'])
                    ctrib += row['CONTRIBUTING FACTOR VEHICLE 4'] + "," 
                if row['CONTRIBUTING FACTOR VEHICLE 5'] != '':
                    contribs.append(row['CONTRIBUTING FACTOR VEHICLE 5'])
                    ctrib += row['CONTRIBUTING FACTOR VEHICLE 5']

                colls[date_time] = (lat, lon, ctrib)

                # Look for the 'Pavement Defective' flag, for collisions
                # that explicitly cite a road condition as a contributing factor
                
                if re.search(r'Pavement Defective',ctrib):
                    colls_pavement[date_time] = (lat, lon, ctrib)    

        except Exception:
            print sys.exc_traceback.tb_lineno
            print row['LOCATION']
            break



print "collisions: " + str(len(colls))

contribs = set(contribs)

print "contributing factors: " + str(len(contribs))
print contribs

print "collisions: bad pavement: " + str(len(colls_pavement))
