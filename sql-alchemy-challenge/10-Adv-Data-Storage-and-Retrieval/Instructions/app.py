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
    
    
    session = Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()
    session.close()
    
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
    
    session = Session(engine)
    unique_stations = session.query(Measurement.station).distinct().all()
    session.close()

    unique_station_list = list(np.ravel(unique_stations))
    return jsonify (unique_station_list)





# tobs route

@app.route('/api/v1.0/tobs')
def tobs():
    
    session = Session(engine)
    year_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', 
                                                                          Measurement.date > '2016-08-18').all()
    session.close()

    tobs_json = []


    for date, tobs in year_temps:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        
        tobs_json.append(tobs_dict)
    
    return jsonify(tobs_json)



# start route 

@app.route('/api/v1.0/<start>')
def temps(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    session = Session(engine)

    tobs_min = session.query(Measurement.date, func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    tobs_avg = session.query(Measurement.date, func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    tobs_max = session.query(Measurement.date, func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    tobs_json = []
    for date,tobs in tobs_min:
        min_dict = {}
        min_dict["date"] = date
        min_dict["minimum tobs"] = tobs
        tobs_json.append(min_dict)
    
    for date,tobs in tobs_avg:
        avg_dict = {}
        avg_dict["date"] = date
        avg_dict["average tobs"] = tobs
        tobs_json.append(avg_dict)
    
    for date,tobs in tobs_max:
        max_dict = {}
        max_dict["date"] = date
        max_dict["maximum tobs"] = tobs
        tobs_json.append(max_dict)
    
    return jsonify(tobs_json)
        
@app.route('/api/v1.0/<start>/<end>')
def temp(start, end):

    session = Session(engine)

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    
    tobs_min = session.query(Measurement.station,
                                    Station.name,
                                    Measurement.date,
                                    func.min(Measurement.tobs)).\
        filter(Measurement.station == Station.station).\
        filter(Measurement.date.between(start_date, end_date)).all()
    
    
    tobs_avg = session.query(Measurement.station,
                                    Station.name,
                                    Measurement.date,
                                    func.avg(Measurement.tobs)).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.date.between(start_date, end_date)).all()
   
    tobs_max = session.query(Measurement.station,
                                    Station.name,
                                    Measurement.date,
                                    func.max(Measurement.tobs)).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.date.between(start_date, end_date)).all()
    session.close()
    tobs_json = []
    for station, name, date, tobs in tobs_min:
        min_dict = {}
        min_dict["station"] = station
        min_dict["name"] = name
        min_dict["date"] = date
        min_dict["minimum tobs"] = tobs
        tobs_json.append(min_dict)

    for station, name, date, tobs in tobs_avg:
        avg_dict = {}
        avg_dict["station"] = station
        avg_dict["name"] = name
        avg_dict["date"] = date
        avg_dict["average tobs"] = tobs
        tobs_json.append(avg_dict)
        
    for station, name, date, tobs in tobs_max:
        max_dict = {}
        max_dict["station"] = station
        max_dict["name"] = name
        max_dict["date"] = date
        max_dict["maximum tobs"] = tobs
        tobs_json.append(max_dict)
    
    # Return JSON representation of list
    return jsonify(tobs_json)

if __name__ == "__main__":
    app.run(debug=True)