from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt



#----------------------------------------

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()
# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



#----------------------------------------

# Perform a query to retrieve the data and precipitation scores
prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()
prcp_data



#----------------------------------------
temps_station = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').all()


#----------------------------------------
year_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', 
                                                                     Measurement.date > '2016-08-18').all()

#----------------------------------------






#Flask app


from flask import Flask, jsonify

app = Flask(__name__)



# Index route

@app.route('/')
def home():
    return "/api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/<start>, /api/v1.0/<start>/<end>"



# precipitation route

@app.route('/api/v1.0/precipitation')
def prcp():
    
    prcp_json = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        
        prcp_json.append(prcp_dict)
    
    return jsonify(prcp_json)





# stations route 

@app.route('/api/v1.0/stations')
def stations():
    unique_station_list = list(np.ravel(unique_stations))
    return jsonify (unique_station_list)





# tobs route

@app.route('/api/v1.0/tobs')
def tobs():
    tobs_json = []
    for date, tobs in year_temps:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        
        tobs_json.append(tobs_dict)
    
    return jsonify(tobs_json)



# start route 

# @app.route('/api/v1.0/<start>')
# def temps(start):
#     temps_query_start = session.query(func.min(Measurement.tobs),
#                    func.max(Measurement.tobs),
#                    func.avg(Measurement.tobs)).filter(func.strptime(Measurement.date, '%Y-%m-%d') >= func.strptime(start,'%Y-%m-%d')).all()
    
#     temps_json = [{'low': x[0], 'high': x[1], 'average': x[2]} for x in temps_query_start]
#     return jsonify(temps_json)





if __name__ == "__main__":
    app.run(debug=True)