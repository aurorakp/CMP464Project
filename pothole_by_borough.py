from __future__ import division
import math, csv, re, sys
from datetime import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from statistics import *
import seaborn as sns
import numpy as np
from bokeh.charts import Bar, BoxPlot
from bokeh.plotting import figure, show, output_file, vplot, hplot
import pandas as pd


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
print ""


nonzero_closed_df = closed_df[(closed_df['timedays'] != 0)]
closed_df_positives = closed_df[(closed_df['timedays'] > 0)]
within_three_stdv = closed_df[(closed_df['timedays'] < (mean_datetime + stdv_datetime*3))]

boxp1 = BoxPlot(closed_df, 'borough', values='timedays', title = "Total Report Time by Borough")
#boxp2 = BoxPlot(nonzero_closed_df, 'borough', values='timedays', title = "Total Report Time by Borough")
#boxp3 = BoxPlot(closed_df_positives, 'borough', values='timedays', title = "Total Report Time by Borough")
outliers = BoxPlot(within_three_stdv, 'borough', values='timedays', title = "TRT Within Three Standard Deviations")

#p1 = hplot(boxp1, boxp2, boxp3)
p1 = hplot(boxp1, outliers)
show(p1)

closed_df_std1 = closed_df[(closed_df['timedays'] > (mean_datetime + stdv_datetime))]
closed_df_std2 = closed_df[(closed_df['timedays'] > (mean_datetime + stdv_datetime*2))]
closed_df_std3 = closed_df[(closed_df['timedays'] > (mean_datetime + stdv_datetime*3))]

nonzeroclosed_df_std1 = closed_df_std1[(closed_df_std1['timedays'] != 0)]
nonzeroclosed_df_std2 = closed_df_std2[(closed_df_std2['timedays'] != 0)]
nonzeroclosed_df_std2 = closed_df_std3[(closed_df_std3['timedays'] != 0)]







