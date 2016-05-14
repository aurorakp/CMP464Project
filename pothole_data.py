# Aurora Koch-Pongsema
# CMP 464: Spring 2016
# Project: Data Collection
# Pothole/Street Condition Data Set

import math, csv, re
from matplotlib import pyplot as plt
from collections import Counter
from datetime import datetime as dt
import sys

# Data downloaded as of 4/17/2016 - note that some potholes, etc., may be
# closed at this point that are open


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

print "Closed potholes with closed dates: " + str(len(closed_date))
print "Closed potholes with no close date: " + str(len(closed_no_date))
print "Assigned pothoes: " + str(len(assigned))
print "Open pothole reports: " + str(len(open_still))
print "Unspecified potholes: " + str(len(unspec))

    
