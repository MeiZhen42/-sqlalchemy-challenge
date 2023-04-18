import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///challenge-10.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Passenger = Base.classes.passenger

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)

session = db
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def start():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/stations<br/>"
        f"/tobs<br/>"
        f"/yyyy-mm-dd<br/>"
        f"/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/precipitation")
def water():

    """Return a list of precipitation for last year"""
    first_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    precip = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > first_year).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_names = {key: value for key, value in precip} # for key and value in precip, value is key

    return jsonify(all_names)


@app.route("/stations")
def passengers():
    stations = session.query(station.station).all()
    
    session.close()

    stations = list(np.ravel(stations)) # returns 1D array and puts it in a list
    
    return jsonify(stations)

@app.route("/tobs")
def passengers():
    first_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    actv = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).all()

    recent = session.query(measurement.tobs).\
    filter(measurement.station == actv[0][0]).\
    filter(measurement.date >= first_year).all()
        
    session.close()

    recent = list(np.ravel(recent)) # returns 1D array and puts it in a list
    
    return jsonify(recent)

@app.route("/<start>") # parse date e.g. dt.datetime.strptime, add if statement e.g. if not end
@app.route("/<start>/<end>")
def passengers(start = None, end = None):
    # Query min temp, average temp, max temp for specified start or start/end range
    # User imput into proper format
    start = session.query(dt.datetime.strptime(time, "yyyy-mm-dd").date()
    end = dt.datetime.strptime(end, 'yyyy-mm-dd').date() # strptime() creates a datetime object from the given string   
    if not end:
        min_temp = session.query(func.min(measurement.tobs)).\
            filter(measurement.date >= start).scalar() 
            
        max_temp = session.query(func.max(measurement.tobs)).\
            filter(measurement.date >= start).scalar()
        av_temp = session.query(func.round(func.avg(measurement.tobs)), 2).\
            filter(measurement.date >= start).scalar()
        
        return jsonify({'Lowest Temperature':min_temp, 
                        'Highest Temperature': max_temp, 
                        'Average Temperature' :av_temp})
    #start and end date section of function
    min_temp = session.query(func.min(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).scalar()
    max_temp = session.query(func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).scalar()
    av_temp = session.query(func.round(func.avg(measurement.tobs)),2).\
        filter(measurement.date >= start).filter(measurement.date <= end).scalar()
    return jsonify({'Lowest Temperature':min_temp, 
                        'Highest Temperature': max_temp, 
                        'Average Temperature' :av_temp})
        
    
    session.close()

# start the app
if __name__ == '__main__':
    app.run(debug=True)