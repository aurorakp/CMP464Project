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
from bokeh.embed import components


def datetime(x):
    return np.array(x, dtype=np.datetime64)

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



nonzero_tuples = [closed_tuples[i] for i in range(len(closed_tuples)) if (closed_tuples[i][-1]!=0)]
sorted_cltup = sorted(closed_tuples, key = lambda tup: tup[-1])
datetimes = [sorted_cltup[x][-1] for x in range(len(sorted_cltup))]
nz_sorted_cltup = sorted(nonzero_tuples, key = lambda tup: tup[-1])
nz_datetimes = [nz_sorted_cltup[x][-1] for x in range(len(nz_sorted_cltup))]


# to compare datetimes, convert them into seconds
seconds = [datetimes[x].total_seconds() for x in range(len(datetimes))]
nz_seconds = [nz_datetimes[x].total_seconds() for x in range(len(nz_datetimes)) if nz_datetimes[x].total_seconds != 0]
print " length of original seconds list: " + str(len(seconds))

# get rid of the 'instantly closed' potholes:

nonzero_sec = [seconds[i] for i in range(len(seconds)) if (seconds[i] != 0)]
print " length of nonzero seconds list: " + str(len(nonzero_sec))

#seconds_index = [i for i in range(len(datetimes))]
nz_minutes = [nz_seconds[i]/60 for i in range(len(nz_seconds))]
nz_hours = [nz_minutes[i]/60 for i in range(len(nz_minutes))]
nz_days = [nz_hours[i]/24 for i in range(len(nz_hours))]
#days_index = [i for i in range(len(days))]
nz_days_index = [i for i in range(len(nz_days))]

#p1 = sns.distplot(nz_days)
output_file("time_to_closed_status.html")

p1 = figure(plot_width=400, plot_height=400, x_axis_type="datetime", y_axis_type="datetime")
p1.xaxis.axis_label = "Created Date"
p1.yaxis.axis_label = "Closed Date"
x1 = [closed_tuples[i][0] for i in range(len(closed_tuples))]
y1 = [closed_tuples[i][-2] for i in range(len(closed_tuples))]
p1.line(x1,y1,line_width=2, color="navy")

p2 = figure(plot_width=400, plot_height=400, x_axis_type="datetime", y_axis_type="datetime")
p2.xaxis.axis_label = "Created Date"
p2.yaxis.axis_label = "Closed Date"
x2 = [nonzero_tuples[i][0] for i in range(len(nonzero_tuples))]
y2 = [nonzero_tuples[i][-2] for i in range(len(nonzero_tuples))]
p2.line(x2,y2,line_width=2, color="firebrick")

p = hplot(p1,p2)

script, div = components(p)
print (script)
print (div)





#nz_x = nz_days
nz_x = nz_minutes
nz_mean_datetime = mean(nz_x)
nz_mode_datetime = mode(nz_x)
nz_range_datetime = data_range(nz_x)
nz_stdv_datetime = standard_deviation(nz_x)
nz_iqr = interquartile_range(nz_x)
nz_mx = max(nz_x)


print " mean is: " + str(nz_mean_datetime)
print " mode is: " + str(nz_mode_datetime)
print " range is: " + str(nz_range_datetime)
print " stdv is: " + str(nz_stdv_datetime)
print " iqr is: " + str(nz_iqr)
print " lowest value is: " + str(nonzero_sec[0])
print " max is: " + str(nz_mx)

nz_1stdv = nz_stdv_datetime
above_1stdev_tup = [nonzero_tuples[i] for i in range(len(nonzero_tuples)) if (nonzero_tuples[i][-1].total_seconds() > nz_1stdv)]


m = Basemap(projection='tmerc',width=55000,height=55000,lon_0=-74.0059,lat_0=40.7127,resolution='h')
m.drawcounties()
m.fillcontinents(color='lemonchiffon',lake_color='#99ffff')

#pot_lons = [nonzero_tuples[i][1] for i in range(len(nonzero_tuples))]
#pot_lats = [nonzero_tuples[i][0] for i in range(len(nonzero_tuples))]
#pot_lons = [iqr_tuples[i][2] for i in range(len(iqr_tuples))]
#pot_lats = [iqr_tuples[i][1] for i in range(len(iqr_tuples))]
pot_lons = [above_1stdev_tup[i][2] for i in range(len(above_1stdev_tup))]
pot_lats = [above_1stdev_tup[i][1] for i in range(len(above_1stdev_tup))]

m.scatter(pot_lons,pot_lats,latlon=True,marker='o',color='b',zorder=10)
plt.title("Potholes Open - 1st Standard Deviation")
plt.show()

# In this part, I'm examining the nonzero tuples, as reports closed immediately upon
# entry indicate a duplicate pothole or report.


output_file("boroughs_by_standard_deviations.html")

# All boroughs, all nonzero data:

#iter_csv = pd.read_csv(data_file, iterator=True, chunksize=1000)
#data_frame = pd.concat([chunk[chunk['Descriptor'] == 'Pothole'] for chunk in iter_csv])
data_frame = pd.read_csv(data_file)
dlframe = data_frame[(data_frame['Location'] != ' ')]
dcframe = dlframe[(dlframe['Status'] == 'Closed')]
dtframe = dcframe[pd.notnull(dcframe['Closed Date'])]
dframe = dtframe[pd.notnull(dtframe['Created Date'])]

print list(dframe.columns.values)
timedeltas = []
crdate = dframe['Created Date'].tolist()
print "crdate[0] is: " + crdate[0]
cldate = dframe['Closed Date'].tolist()
print "cldate[0] is: " + cldate[0]

for i in range(len(dframe)):
    cld = dt.strptime(str(cldate[i]), '%m/%d/%Y %I:%M:%S %p')
    crd = dt.strptime(str(crdate[i]), '%m/%d/%Y %I:%M:%S %p')
    #print cld
    #print crd
    timedelta = dt.strptime(cldate[i], '%m/%d/%Y %I:%M:%S %p') - dt.strptime(crdate[i], '%m/%d/%Y %I:%M:%S %p')
    timedeltas.append(timedeltas)
    

dframe['timedelta'] = timedeltas


barp = BoxPlot(dframe, 'Borough', values='timedelta', title = "Report Time by Borough")


script1, div1 = components(barp)
print (script1)
print (div1)


##mh_nz = [above_1stdev_tup[i][-1] for i in range(len(above_1stdev_tup)) if above_1stdev_tup[i][3] == 'MANHATTAN']
##mh_nz_closed = [nonzero_tuples[i][-2] for i in range(len(nonzero_tuples)) if nonzero_tuples[i][3] == 'MANHATTAN']
##mh_nz_closed_ind = [i for i in range(len(mh_nz_closed))]
##mh_nz_created = [nonzero_tuples[i][0]for i in range(len(nonzero_tuples)) if nonzero_tuples[i][3] == 'MANHATTAN']
##mh_nz_created_sorted = sorted(mh_nz_created)
##mh_nz_created_sorted_original_index = sorted(range(len(mh_nz_created_sorted)), key = lambda k: mh_nz_created_sorted[k])
##mh_closed_by_original_index_sort = []
##for i in range(len(mh_nz_created_sorted_original_index)):
##    ind = mh_nz_created_sorted_original_index[i]
##    mh_closed_by_original_index_sort.append(mh_nz_created_sorted_original_index[ind])
##sortrange = [i for i in range(len(mh_closed_by_original_index_sort))]
##
##
##p1 = figure(y_axis_type = "datetime")
##
###p1.line(mh_nz_closed_ind, datetime(mh_nz_closed))
###p1.line(mh_nz_closed_ind, mh_nz_closed,line_color='blue')
###p1.line(mh_nz_closed_ind, mh_nz_created_sorted,line_color='red')
##p1.line(sortrange, mh_nz_created_sorted, line_color='red')
##p1.line(sortrange, mh_closed_by_original_index_sort, line_color='blue')
##output_file("test.html", title="datetimes for manhattan")
##show(vplot(p1))


