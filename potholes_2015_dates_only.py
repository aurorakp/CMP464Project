import math, csv, re
from matplotlib import pyplot as plt
from collections import Counter
from datetime import datetime as dt
import sys
from sklearn import linear_model
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show

data_file = "311_StreetCondition_2015.csv"

potholes = []
closed_potholes = []
open_potholes = []

with open(data_file,'rU') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        year_dt = dt.strptime('01/01/2015 12:00:00 AM','%m/%d/%Y %I:%M:%S %p')
        cldt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
        if row['Status']=='Closed':
            status = 0
        else:
            status = 1
        potholes.append((cldt, status))
    

x = [potholes[i][0] for i in range(len(potholes))]
y = [potholes[i][1] for i in range(len(potholes))]

# Note: Used the example from the scikit learn for this part:
# http://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic.html

output_file("created_and_closed_dates.html")

p1 = figure(plot_width=600, plot_height=600, x_axis_type="datetime")
p1.xaxis.axis_label = "Created Date"
p1.yaxis.axis_label = "Pothole Status"
#p1.line(x,y,line_width=2, color="navy")
p1.circle(x,y,size=5, color="firebrick", alpha=0.5)
show(p1)

