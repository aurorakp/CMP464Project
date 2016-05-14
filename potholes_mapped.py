from __future__ import division
import math, csv, re, sys
from datetime import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from statistics import *
import seaborn as sns
import numpy as np
from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, ResetTool
)
from bokeh.charts import Bar, BoxPlot
from bokeh.plotting import figure, show, output_file, vplot, hplot
import pandas as pd
from collections import Counter


def datetime(x):
    return np.array(x, dtype=np.datetime64)

data_file = "311_StreetCondition_2015.csv"



output_file("boroughs_by_standard_deviations.html")

# All boroughs, all nonzero data:

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
                    bor = row['Borough']
                    
                    closed_date[created_dt] = (lat, lon, bor, closed_dt, closed_dt - created_dt)
                    closed_tuples.append((created_dt, lat, lon, bor, closed_dt, closed_dt - created_dt))
            else:
                pass
                 
            
        except ValueError as v:
            print sys.exc_traceback.tb_lineno
            break

created_dates = [closed_tuples[i][0] for i in range(len(closed_tuples))]
closed_dates = [closed_tuples[i][-2] for i in range(len(closed_tuples))]
closed_boroughs = [closed_tuples[i][-3] for i in range(len(closed_tuples))]
closed_lats = [closed_tuples[i][1] for i in range(len(closed_tuples))]
closed_lons = [closed_tuples[i][2] for i in range(len(closed_tuples))]
closed_timedeltas = [closed_tuples[i][-1] for i in range(len(closed_tuples))]
# to get the conversion to days, convert to seconds, then divide by
# 60 seconds/minute, 60 minutes/hr, and 24 hrs/day
closed_timedays = [closed_timedeltas[i].total_seconds()/(60*60*24) for i in range(len(closed_timedeltas))]

closed_d = {'cldate' : pd.Series(closed_dates, index = created_dates),
     'borough' : pd.Series(closed_boroughs, index = created_dates),
     'lat' : pd.Series(closed_lats, index = created_dates),
     'lon' : pd.Series(closed_lons, index = created_dates),
     'timedelta' : pd.Series(closed_timedeltas, index = created_dates),
     'timedays' : pd.Series(closed_timedays, index = created_dates)}

closed_df = pd.DataFrame(closed_d)

x = closed_timedays
mean_datetime = mean(x)
mode_datetime = mode(x)
range_datetime = data_range(x)
stdv_datetime = standard_deviation(x)
iqr = interquartile_range(x)

print " mean is: " + str(mean_datetime)
print " mode is: " + str(mode_datetime)
print " range is: " + str(range_datetime)
print " stdv is: " + str(stdv_datetime)
print " iqr is: " + str(iqr)
print " 1st std dv away from mean is: " + str(mean_datetime + stdv_datetime)
print " 2nd std dv away from mean is: " + str(mean_datetime + stdv_datetime*2)
print " 3rd std dv away from mean is: " + str(mean_datetime + stdv_datetime*3)

nonzero_closed_df = closed_df[(closed_df['timedays'] != 0)]
closed_df_positives = closed_df[(closed_df['timedays'] > 0)]


closed_df_std1 = closed_df[(closed_df['timedays'] > (mean_datetime + stdv_datetime))]
closed_df_std2 = closed_df[(closed_df['timedays'] > (mean_datetime + stdv_datetime*2))]
closed_df_std3 = closed_df[(closed_df['timedays'] > (mean_datetime + stdv_datetime*3))]


nonzeroclosed_df_std1 = closed_df_std1[(closed_df_std1['timedays'] != 0)]
nonzeroclosed_df_std2 = closed_df_std2[(closed_df_std2['timedays'] != 0)]
nonzeroclosed_df_std2 = closed_df_std3[(closed_df_std3['timedays'] != 0)]

closed_lats_std1 = closed_df_std1['lat'].tolist()
closed_lats_std2 = closed_df_std2['lat'].tolist()
closed_lats_std3 = closed_df_std3['lat'].tolist()

closed_lons_std1 = closed_df_std1['lon'].tolist()
closed_lons_std2 = closed_df_std2['lon'].tolist()
closed_lons_std3 = closed_df_std3['lon'].tolist()

bor = closed_df['borough'].tolist()
bor_std1 = closed_df_std1['borough'].tolist()
bor_std2 = closed_df_std2['borough'].tolist()
bor_std3 = closed_df_std3['borough'].tolist()

b = Counter(bor)
print "Borough counts (all potholes): "
print b
print "Total potholes: " + str(len(bor))
b1 = Counter(bor_std1)
print "Borough counts (potholes longer than 1 stdv): "
print b1
print "Total potholes longer than 1 stdv: " + str(len(bor_std1))
b2 = Counter(bor_std2)
print "Borough counts (potholes longer than 1 stdv): "
print b2
print "Total potholes longer than 1 stdv: " + str(len(bor_std2))
b3 = Counter(bor_std3)
print "Borough counts (potholes longer than 1 stdv): "
print b3
print "Total potholes longer than 1 stdv: " + str(len(bor_std3))


# How to do this:
# http://bokeh.pydata.org/en/0.11.1/docs/user_guide/geo.html

output_file("gmap_plot.html")

map_options = GMapOptions(lat=40.7127, lng=-74.0059, map_type="hybrid", zoom=10)

plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Potholes Open Past Days")

source = ColumnDataSource(data=dict(lat=closed_lats, lon=closed_lons))

circle = Circle(x="lon",y="lat", size=2, fill_color="blue", fill_alpha=0.8, line_color=None)
circle_larger = Circle(x="lon",y="lat", size=5, fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), ResetTool())


plot1 = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Potholes Open Past Days")
source1 = ColumnDataSource(data=dict(lat=closed_lats_std1, lon=closed_lons_std1))
plot1.add_glyph(source1, circle)
plot1.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), ResetTool())

plot2 = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Potholes Open Past Days")
source2 = ColumnDataSource(data=dict(lat=closed_lats_std2, lon=closed_lons_std2))
plot2.add_glyph(source2, circle)
plot2.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), ResetTool())

plot3 = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Potholes Open Past Days")
source3 = ColumnDataSource(data=dict(lat=closed_lats_std3, lon=closed_lons_std3))
plot3.add_glyph(source3, circle_larger)
plot3.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), ResetTool())

p1 = hplot(plot, plot1)
p2 = hplot(plot2, plot3)
p = vplot(p1, p2)
show(p)
