from __future__ import division
import math, csv, re, sys
from datetime import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from statistics import *
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, ResetTool
)
from bokeh.charts import Bar, BoxPlot
from bokeh.plotting import figure, show, output_file, vplot, hplot
import pandas as pd

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
                borough = row['BOROUGH']
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

                colls[date_time] = (lat, lon, borough, ctrib)

                # Look for the 'Pavement Defective' flag, for collisions
                # that explicitly cite a road condition as a contributing factor
                
                if re.search(r'Pavement Defective',ctrib):
                    colls_pavement[date_time] = (lat, lon, borough, ctrib)    

        except Exception:
            print sys.exc_traceback.tb_lineno
            print row['LOCATION']
            break

coll_lats = []
coll_lons = []
coll_dists = []
coll_bors = []

# See where the pavement was cited as a 'reason for collision'

for coll in colls_pavement.values():
        coll_lats.append(coll[0])
        coll_lons.append(coll[1])
        coll_dists.append((coll[0],coll[1]))
        coll_bors.append(coll[2])

data_file = "311_StreetCondition_2015.csv"

closed_date = {}
closed_tuples = []
resolutions = []

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
                    closed_date[created_dt] = (lat, lon, closed_dt, closed_dt - created_dt)
                    closed_tuples.append((created_dt, lat, lon, closed_dt, closed_dt - created_dt))
            else:
                pass
                 
            
        except ValueError as v:
            print sys.exc_traceback.tb_lineno
            break



nonzero_tuples = [closed_tuples[i] for i in range(len(closed_tuples)) if (closed_tuples[i][-1]!=0)]
nonzero_tuples_loc = [(closed_tuples[i][1],closed_tuples[i][2]) for i in range(len(closed_tuples)) ]
print "nonzero_tuples_loc is length " + str(len(nonzero_tuples_loc))
print "nonzero_tuples_loc[0] = " + str(nonzero_tuples_loc[0])
print "nonzero_tuples_loc[0][0] = " + str(nonzero_tuples_loc[0][0])

nz_dt = [closed_tuples[i][-1].total_seconds() for i in range(len(closed_tuples))]
nz_mn = mean(nz_dt)
nz_stdv = standard_deviation(nz_dt)
#nz_2stdv = nz_mn + 3*nz_stdv
#nz_2stdv = nz_mn + 2*nz_stdv
nz_2stdv = nz_mn + 1*nz_stdv


colls_with_pothole_reported = []
colls_pv = colls_pavement.values()


##for coll in colls_pavement.values():
##    (lat, lon) = (coll[0],coll[1])
##    
##    if (lat, lon) in nonzero_tuples_loc:
##        colls_with_pothole_reported.append(coll)

coll_lons = [colls_with_pothole_reported[i][1] for i in range(len(colls_with_pothole_reported))]
coll_lats = [colls_with_pothole_reported[i][0] for i in range(len(colls_with_pothole_reported))]
coll_pv_lons = [colls_pv[i][1] for i in range(len(colls_pavement))]
coll_pv_lats = [colls_pv[i][0] for i in range(len(colls_pavement))]
output_file("pothole_related_collisions.html")

print "number of collisions due to pavement: " + str(len(coll_bors))
b = Counter(coll_bors)
print b



map_options = GMapOptions(lat=40.7127, lng=-74.0059, map_type="hybrid", zoom=10)

plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Potholes Open Past Days")

source = ColumnDataSource(data=dict(lat=coll_pv_lats, lon=coll_pv_lons))

circle = Circle(x="lon",y="lat", size=2, fill_color="blue", fill_alpha=0.8, line_color=None)
circle_larger = Circle(x="lon",y="lat", size=5, fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle_larger)
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), ResetTool())

show(plot)

##m = Basemap(projection='tmerc',width=55000,height=55000,lon_0=-74.0059,lat_0=40.7127,resolution='h')
##m.drawcounties()
##m.fillcontinents(color='lemonchiffon',lake_color='#99ffff')
###m.scatter(coll_lons,coll_lats,latlon=True,marker='o',color='b',zorder=10)
##m.scatter(coll_pv_lons,coll_pv_lats, latlon=True,marker='o',color='b',zorder=10)
##plt.title("Collisions Reportedly Due To Defective Pavement")
##plt.show()

nonzero_tuples_loc_rounded = []
collvals = [(colls_pv[i][0], colls_pv[i][1]) for i in range(len(colls_pavement))]
print("collvals length is: " + str(len(collvals)))

for i in range(len(nonzero_tuples_loc)):
    lat,lon = nonzero_tuples_loc[i][0],nonzero_tuples_loc[i][1]
    #print "lat is: " + str(lat)
    nlat = round(lat, 2)
    nlon = round(lon, 2)
    nonzero_tuples_loc_rounded.append((nlat, nlon))

for i in range(len(collvals)):
    (lat, lon) = collvals[i][0], collvals[i][0]
    
    lat = round(lat, 2)
    lon = round(lon, 2)
    
    if (lat, lon) in nonzero_tuples_loc_rounded:
        print str(lat) + " " + str(lon)
        



##print "reported length : " + str(len(colls_with_pothole_reported))
##
##reported = [colls_with_pothole_reported[i] for i in range(len(colls_with_pothole_reported))]
##reported_dt = [reported[i][-1].total_seconds() for i in range(len(reported))]
##reported_days = [reported_dt[i]/(60*60) for i in range(len(reported_dt))]
##rep_mn = mean(reported_days)
##rep_stdv = standard_deviation(reported_days)
##rep_1stdv = rep_mn + rep_stdv
##rep_2stdv = rep_mn + 2 * rep_stdv
##rep_3stdv = rep_mn + 3 * rep_stdv
##print "Mean days for potholes where a collision was reported to be fixed: " + str(rep_mn)
##print "Stdv: " + str(rep_stdv)
##print "1st stdv: " + str(rep_1stdv)
##print "2nd stdv: " + str(rep_2nddv)
##print "3rd stdv: " + str(rep_3rddv)
##print " range is: " + str(data_range(reported_days))

##coll_pv_dist = []
##for i in range(len(colls_pv)):
##    coll_pv_dist.append([colls_pv[i][1], colls_pv[i][0]])
##    print [colls_pv[i][1], colls_pv[i][0]]
##
##coll_pv_dist = [[colls_pv[i][1] , colls_pv[i][0]] for i in range(len(colls_pavement))]
##points = np.array(coll_pv_dist)
##pv_vor = Voronoi(points)
##voronoi_plot_2d(pv_vor)
##plt.title("Voronoi diagram of Collisions due to Defective Pavement")
##plt.show()
