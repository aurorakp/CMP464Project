
import math, csv, re, sys
from datetime import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



# Collisions

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


# Potholes

data_file = "311_StreetCondition_2015.csv"

closed_date = {}        # Pothole report is closed, has closed date
closed_no_date = {}     # Pothole report is closed, no closed date
assigned = {}           # Pothole report assigned
open_still = {}         # Pothole report is open
unspec = {}             # Pothole report is 'unspecified'

with open(data_file,'rU') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        try:
            if row['Location'] != '' and row['Descriptor'] == 'Pothole':
                if row['Status'] == 'Closed' and row['Closed Date'] != '':
                    crdt = row['Created Date']
                    created_dt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
                    cldt = row['Closed Date']
                    closed_dt = dt.strptime(row['Closed Date'], '%m/%d/%Y %I:%M:%S %p')
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    assn_note = row['Resolution Description']
                    closed_date[crdt] = (lat, lon, assn_note, cldt)
                elif row['Status'] == 'Assigned' or row['Status'] == 'Pending':
                    crdt = row['Created Date']
                    created_dt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
                    assn_note = row['Resolution Description']
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    assigned[crdt] = (lat, lon, assn_note)
                elif row['Status'] == 'Unspecified':
                    crdt = row['Created Date']
                    created_dt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
                    assn_note = row['Resolution Description']
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    unspec[crdt] = (lat, lon, assn_note)
                elif row['Status'] == 'Open':
                    crdt = row['Created Date']
                    created_dt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
                    assn_note = row['Resolution Description']
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    open_still[crdt] = (lat, lon, assn_note)
                else:
                    crdt = row['Created Date']
                    created_dt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
                    assn_note = row['Resolution Description']
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    closed_no_date[crdt] = (lat, lon, assn_note)
            else:
                pass
                 
            
        except ValueError as v:
            print sys.exc_traceback.tb_lineno
            break

coll_lats = []
coll_lons = []

for coll in colls.values():
    coll_lats.append(coll[0])
    coll_lons.append(coll[1])


pot_lats = []
pot_lons = []


#pot_list = [closed_date, closed_no_date, assigned, open_still, unspec]

for p in closed_date.values():
    pot_lats.append(p[0])
    pot_lons.append(p[1])
for p in closed_no_date.values():
    pot_lats.append(p[0])
    pot_lons.append(p[1])
for p in assigned.values():
    pot_lats.append(p[0])
    pot_lons.append(p[1])
for p in open_still.values():
    pot_lats.append(p[0])
    pot_lons.append(p[1])
for p in unspec.values():
    pot_lats.append(p[0])
    pot_lons.append(p[1])

    

m = Basemap(projection='tmerc',width=55000,height=55000,lon_0=-74.0059,lat_0=40.7127,resolution='h')
m.drawcounties()
m.fillcontinents(color='lemonchiffon',lake_color='#99ffff')

m.scatter(coll_lons,coll_lats,latlon=True,marker='o',color='b',zorder=10)
m.scatter(pot_lons,pot_lats,latlon=True,marker='o',color='r',zorder=10)

plt.show()
