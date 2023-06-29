import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, jsonify


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
    return render_template('index.html')

@app.route("/api/v1.0/AZ")
def allData():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Convert the query results from your heat days Apache analysis
    allData = session.query(ExHt.key, ExHt.county, ExHt.year, ExHt.ext_heat_days).\
        order_by(ExHt.county).all()
    
    session.close()

    # analysis to a dictionary using year as the key and ext as the value.
    all_query_values = []
    
    # Create list with column names
    cNames= ["key", "county", "year", "ext_heat_days"]

    # enumerate- returns index & element
    for element in allData:
        my_dict = {}
        
        for index1, element1 in enumerate(cNames):
            my_dict[element1] = element[index1]
            
        all_query_values.append(my_dict)

    
    return jsonify(all_query_values)
    # this returns too much for the list. Want it something like ExHt.county
    # then listed below 

@app.route("/api/v1.0/counties")
def counties():
    
    # Open session
    session = Session(engine)
    
    # Query all counties 
    results = session.query(ExHt.county).distinct().all()

    # close session
    session.close()

      # Convert list of tuples into normal list
    all_counties = list(np.ravel(results))

    return jsonify(all_counties)

@app.route("/api/v1.0/AZ2021")
def twentyone():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Convert the query results from your heat days Apache analysis
    All_ehd = session.query(ExHt.county, ExHt.ext_heat_days).\
        filter(ExHt.year == '2021').\
        order_by(ExHt.county).all()
    
    session.close()

    # analysis to a dictionary using year as the key and ext as the value.
    twentyone_query_values = []
    for second, first in All_ehd:
        All_ehd_dict = {}
        All_ehd_dict["county"] = second
        All_ehd_dict["ext_heat_days"] = first
        twentyone_query_values.append(All_ehd_dict)

    return jsonify(twentyone_query_values)
    # return render_template("index.html", Apache_query_values=Apache_query_values)


@app.route("/api/v1.0/ApacheCounty")
def ApacheCounty():
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
        Apache_EHD_dict["year"] = two
        Apache_EHD_dict["ext_heat_days"] = one
        Apache_query_values.append(Apache_EHD_dict)

    return jsonify(Apache_query_values)
    # return render_template("index.html", Apache_query_values=Apache_query_values)

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