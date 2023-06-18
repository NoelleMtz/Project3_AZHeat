import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# from flask_cors.extension import CORS
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/hri.sqlite")

# #Reflect an existing database into a new model
Base = automap_base()
# #Reflect the tables
Base.prepare(autoload_with=engine)

# #Save reference to the table

ExHt = Base.classes.extreme_heat_days

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes for AZ extreme hete days:<br/>"
        f"-- Extreme Heat Days for Apache County: <a href=\"/api/v1.0/ApacheCounty\">/api/v1.0/ApacheCounty<a><br/>"
        f"-- Enter a county to get the temperatures for the past 10 years: /api/v1.0/countyID<br>"
    )

@app.route("/api/v1.0/ApacheCounty")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Convert the query results from your heat days Apache analysis
    Apache_ehd = session.query(ExHt.year, ExHt.ext_heat_days).\
        filter(ExHt.county == 'Apache').\
        order_by(ExHt.year).all()
    
    session.close()

    # analysis to a dictionary using year as the key and ext as the value.
    Apache_query_values = []
    for two, one in Apache_ehd:
        Apache_EHD_dict = {}
        Apache_EHD_dict["Year"] = two
        Apache_EHD_dict["Extreme Heat Days"] = one
        Apache_query_values.append(Apache_EHD_dict)

    return jsonify(Apache_query_values) 

# Dynamic Route
@app.route("/api/v1.0/<countyID>")
# Accepts the start date as a parameter from the URL 
def start_route(countyID):
    # the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
    session = Session(engine)
    
    query_result = session.query(ExHt.year, ExHt.ext_heat_days ).\
        filter(ExHt.countyID == countyID).\
        order_by(ExHt.year).all()
        
    session.close()

    # dictionary for specific county
    county_query_values = []
    for two, one in query_result:
        county_ehd_dict = {}
        county_ehd_dict["year"] = two
        county_ehd_dict["ext_heat_days"] = one
        county_query_values.append(county_ehd_dict)

    # If the query returned non-null values return the results,
    # otherwise return an error message
    if county_ehd_dict['ext_heat_days']: 
        return jsonify(county_query_values)
    else:
        return jsonify({"error": f"County {countyID} not found or not formatted without the name County."}), 404
  
  
if __name__ == "__main__":
    app.run(debug=True)