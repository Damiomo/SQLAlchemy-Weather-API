# Import the dependencies.
import sqlalchemy
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)

# Save references to each table
M = Base.classes.measurement
S = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return '''
        <body style='background:beige;margin:0'>
            <h1 style='text-align:center;background:linear-gradient(35deg,teal 40%, black 90%);color:white'>Hawaii's Weather API</h1>
            <h3>The following routes are available:</h3>
            <ul>
                <li><a href='/api/v1.0/precipitation'>Precipitation</a></li>
                <li><a href='/api/v1.0/stations'>Stations</a></li>
                <li><a href='/api/v1.0/tobs'>Temperature Observed</a></li>
                <li><a href='/api/v1.0/2010-01-01'>Can change start date</a></li>
                <li><a href='/api/v1.0/2010-01-01/2017-08-23'>Can change start and end date</a></li>
            </ul>
        </body>
    '''

@app.route('/api/v1.0/precipitation')
def precipitation():
    return { d:p for d,p in session.query(M.date,M.prcp).filter(M.date>='2016-08-23').all()}

@app.route('/api/v1.0/stations')
def stations():
    return { id:loc for id,loc in session.query(S.station,S.name).all()}

@app.route('/api/v1.0/tobs')
def temps():
    return { 
            d:t for d,t in session.query(M.date,M.tobs).filter(
            (M.station=='USC00519281')&
            (M.date>='2016-08-23')
            ).all()
        }

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def dates_range(start,end='2017-08-23'):
    min,avg,max = session.query(
            func.min(M.tobs),
            func.avg(M.tobs),
            func.max(M.tobs)
        ).filter(
            (M.date>=start)&
            (M.date<=end)
        ).first()

    return {
        'Min_Temp':min, 
        'Avg_Temp':avg, 
        'Max_Temp':max, 
        'Start_date':start, 
        'End_date':end
    }

if __name__ == '__main__':
    app.run()