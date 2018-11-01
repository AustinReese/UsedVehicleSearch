#queryForm.py takes data submitted by the user through the form and constructs an sql query to grab data that matches their specifications

import sqlite3
from datetime import datetime
from geopy.geocoders import Nominatim


def queryForm(data):
    #this will be used to get the lat/long of cities, allowing for cars nearby searches
    geo = Nominatim(user_agent="CraigslistFilter")    
    
    #grab data from user
    city = data.city.data
    state = data.state.data
    manu = data.manufacturer.data
    make = data.make.data
    cond = data.condition.data
    cyl = data.cylinders.data
    fuel = data.fuel.data
    tran = data.transmission.data
    title = data.titleStatus.data
    vin = data.vin.data
    drive = data.drive.data
    size = data.size.data
    vType = data.vehicleType.data
    color = data.paintColor.data
    priceStart = data.priceStart.data
    priceEnd = data.priceEnd.data
    yearStart = data.yearStart.data
    yearEnd = data.yearEnd.data
    odomStart = data.odometerStart.data
    odomEnd = data.odometerEnd.data
        
    #construct dict of strings for the query
    criteriaDict = {city: "city", manu: "manufacturer", make: "make", cond: "condition", 
                    cyl: "cylinders", tran: "transmission", vin: "vin", fuel: "fuel",
                    drive: "drive", size: "size", vType: "type", title: "title_status",
                    color: "paint_color", priceStart: "price", priceEnd: "price", yearStart: "year", yearEnd: "year", odomStart: "odometer", odomEnd: "odometer"}
    
    whereClause = ""
    for k, v in criteriaDict.items():
        #if not k then the field was left blank and we do not include it in the query, otherwise we search by it
        if k != None and k != "":
            #these if statements allow for searching by minimum/maximum values
            if v == "year":
                # for example we must handle blank min/max's so if they are blank they are set to the default min/max
                if yearStart == None:
                    yearStart = 1880
                #again with maximum
                if yearEnd == None:
                    yearEnd = datetime.now().year + 1
                #query between the two values
                whereClause = whereClause + "{} BETWEEN '{}' AND '{}' AND ".format(v, yearStart, yearEnd)
            #repeat
            elif v == "odometer":
                if odomStart == None:
                    odomStart = 0
                if odomEnd == None:
                    odomEnd = 10000000
                whereClause = whereClause + "{} BETWEEN '{}' AND '{}' AND ".format(v, odomStart, odomEnd)
            elif v == "price":
                if priceStart == None:
                    priceStart = 0
                if priceEnd == None:
                    priceEnd = 10000000
                whereClause = whereClause + "{} BETWEEN '{}' AND '{}' AND ".format(v, priceStart, priceEnd)
            elif v == "make":
                whereClause = whereClause + "{} CONTAINS {} AND ".format(v, k)
            elif v == "city":
                # all results near a city
                lat, long = 0, 0
                if not state:
                    loc = geo.geocode(city)
                    if loc:
                        lat, long = loc.latitude, loc.longitude
                else:
                    loc = geo.geocode("{}, {}".format(city, state))
                    if loc:
                        lat, long = loc.latitude, loc.longitude
                whereClause = whereClause + "lat BETWEEN '{}' AND '{}' AND long BETWEEN '{}' AND '{}' AND "\
                    .format(lat - .5, lat + .5, long - .5, long + .5)
            elif v == "state" and not criteriaDict["city"]:
                # all results within a state
                pass
            else:
                whereClause = whereClause + "{} LIKE '{}' AND ".format(v, k)
    
    #remove the last AND after the loop completes
    whereClause = whereClause[:-5]
        
    #finally our query
    if not whereClause:
        query = "SELECT * FROM vehicles LIMIT 100;"
    else:
        query = "SELECT * FROM vehicles WHERE {} LIMIT 102;".format(whereClause)
            
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    curs.execute(query)
    res = curs.fetchall()
    db.close()
        
    #return our results
    return res
