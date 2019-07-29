# add dependencies
#import pandas as pd
#import os
import datetime
#import matplotlib.pyplot as plt
#import numpy as np
#import time
from pprint import pprint
#from sqlalchemy import create_engine
#from sqlalchemy.orm import Session
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.ext.automap import automap_base

#from sqlalchemy import Column, Integer, String, Float, and_, Date, desc, func

# PyMySQL 
#import pymysql
#pymysql.install_as_MySQLdb()
import csv
with open("Resources/hawaii_measurements.csv", newline='') as csvfile:
    measurements = []
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader)
    for row in spamreader:
        try: 
            row[2] = float(row[2])
        except ValueError:
            row[2] = 0.0
        row[3] = float(row[3])
        try: 
            row[3] = float(row[3])
        except ValueError:
            row[3] = 0.0
        measurements.append(row)
        
pprint(measurements) 

with open("Resources/hawaii_stations.csv", newline='') as csvfile:
    stations_data = []
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader)
    for row in spamreader:
        row[3] = float(row[3])
        try: 
            row[3] = float(row[3])
        except ValueError:
            row[3] = 0.0
        row[4] = float(row[4])
        try: 
            row[4] = float(row[4])
        except ValueError:
            row[4] = 0.0
        row[5] = float(row[5])
        try: 
            row[5] = float(row[5])
        except ValueError:
            row[5] = 0.0
        stations_data.append(row)
pprint(stations_data) 

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    out = ["/", "/api/v1.0/precipitation", "/api/v1.0/stations", "/api/v1.0/tobs", "/api/v1.0/<start>", "/api/v1.0/<start>/<end>"]
    return jsonify(out)

@app.route("/api/v1.0/precipitation")
def precipitation():
    out = {}
    for row in measurements:
        out[row[1]] = row[2]
    return jsonify(out)

@app.route("/api/v1.0/stations")
def stations():
    out = []
    for row in stations_data:
        out.append(row[0])
    return jsonify(out)

@app.route("/api/v1.0/tobs")
def tobs():
    start_date = "2016-08-23"
    out = []
    for rows in measurements:
        if datetime.date.fromisoformat(start_date) <= datetime.date.fromisoformat(rows[1]):
            out.append(rows[3])
    return jsonify(out)

@app.route("/api/v1.0/<start>")
def temp_stat_start(start):
    out = []
    for rows in measurements:
        if datetime.date.fromisoformat(start) <= datetime.date.fromisoformat(rows[1]):
            out.append(rows[3])
    return jsonify([min(out), sum(out)/len(out), max(out)])

@app.route("/api/v1.0/<start>/<end>")
def temp_stat_startend(start, end):
    out = []
    for rows in measurements:
        if datetime.date.fromisoformat(start) <= datetime.date.fromisoformat(rows[1]) and datetime.date.fromisoformat(end) >= datetime.date.fromisoformat(rows[1]):
            out.append(rows[3])
    return jsonify([min(out), sum(out)/len(out), max(out)])

if __name__ == "__main__":
    app.run(debug=True)