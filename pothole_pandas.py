from __future__ import division
import math, csv, re, sys
from datetime import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from statistics import *
import seaborn as sns
import numpy as np
from bokeh.plotting import figure, show, output_file, vplot
import pandas as pd


def datetime(x):
    return np.array(x, dtype=np.datetime64)

data_file = "311_StreetCondition_2015.csv"


# Use Pandas and Seaborn to make a plot of the borough data
# reference: http://stackoverflow.com/questions/13651117/pandas-filter-lines-on-load-in-read-csv

iter_csv = pd.read_csv(data_file, iterator=True, chunksize=1000)
data_frame = pd.concat([chunk[chunk['Descriptor'] == 'Pothole'] for chunk in iter_csv])
dtframe = data_frame[(data_frame['Location'] != ' ')]
dframe = dtframe[(dtframe['Status'] == 'Closed')]
print list(dframe.columns.values)

# Extract and add the timedeltas to the data frame

timedeltas = []
crdate = dframe.loc['Created Date']
cldate = dframe.loc['Closed Date']

for i in range(len(dframe)):
    timedelta = dt.strptime(cldate[i][0], '%m/%d/%Y %I:%M:%S %p') - dt.strptime(crdate[i][0], '%m/%d/%Y %I:%M:%S %p')
    timedeltas.append(timedeltas)
    

dframe['timedelta'] = timedeltas


sns.set(style="whitegrid")
sns.countplot(x="timedelta",data=dframe, palette="Blues_d")
plt.show()
