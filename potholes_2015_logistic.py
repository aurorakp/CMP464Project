import math, csv, re
from matplotlib import pyplot as plt
from collections import Counter
from datetime import datetime as dt
import sys
from sklearn import linear_model
import numpy as np

data_file = "311_StreetCondition_2015.csv"

potholes = []
closed_potholes = []
open_potholes = []

with open(data_file,'rU') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        if row['Status'] == 'Closed':
            year_dt = dt.strptime('01/01/2015 12:00:00 AM','%m/%d/%Y %I:%M:%S %p')
            cldt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
            # Change the datetime into an object that scikit learn will deal with, i.e. seconds
            # that have passed since the beginning of the year
            created_dt =  (cldt - year_dt).total_seconds()
            # Weed out anomalous close dates (i.e. those closed before the 'created date'
            if created_dt > 0:
                status = 0
                potholes.append((created_dt, status))
                closed_potholes.append((created_dt, status))
        else:
            year_dt = dt.strptime('01/01/2015 12:00:00 AM','%m/%d/%Y %I:%M:%S %p')
            crdt = dt.strptime(row['Created Date'], '%m/%d/%Y %I:%M:%S %p')
            # Change the datetime into an object that scikit learn will deal with, i.e. seconds
            # that have passed since the beginning of the year
            created_dt =  (crdt - year_dt).total_seconds()
            # Weed out anomalous close dates (i.e. those closed before the 'created date'
            if created_dt > 0:
                status = 1
                potholes.append((created_dt, status))
                closed_potholes.append((created_dt, status))
                

x = [potholes[i][0] for i in range(len(potholes))]
y = [potholes[i][1] for i in range(len(potholes))]

# Note: Used the example from the scikit learn for this part:
# http://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic.html

X = np.array(x)
print X.shape
X = X.reshape((-1,1))

print "x is length: " + str(len(x))
print "y is length: " + str(len(y))


clf = linear_model.LogisticRegression()
clf.fit(X,y)

def model(x):
    return 1 / (1+ np.exp(-x))
loss = model(X*clf.coef_ + clf.intercept_).ravel()
#plt.plot(X, loss, color='red')

plt.scatter(X.ravel(),y,color='blue',zorder=20)
plt.title("Logistic Regression of NYC Pothole Status By Date, 2015")
plt.show()
