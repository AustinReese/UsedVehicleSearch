#queryForm.py takes data submitted by the user through the form and constructs an sql query to grab data that matches their specifications

import sqlite3

def queryForm(data):
    
    #grab data from user
    city = data.city.data
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
    price = data.price.data
    year = data.year.data
    odom = data.odometer.data
        
    #construct dict of strings for the query
    criteriaDict = {city: "city", manu: "manufacturer", make: "make", cond: "condition", 
                    cyl: "cylinders", tran: "transmission", vin: "vin", fuel: "fuel",
                    drive: "drive", size: "size", vType: "vehicleType", 
                    color: "paintColor", price: "price", year: "year", odom: "odometer"}
    
    whereClause = ""
    for k, v in criteriaDict.items():
        #if not k then the field was left blank and we do not include it in the query, otherwise we search by it
        if k:
            whereClause = whereClause + "{} LIKE '{}' AND ".format(v, k)
    
    #remove the last AND after the loop completes
    whereClause = whereClause[:-5]
        
    #finally our query
    query = "SELECT * FROM vehicles WHERE {} LIMIT 100;".format(whereClause)
    
    print(query)
        
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    curs.execute(query)
    res = curs.fetchall()
    db.close()
        
    #return our results
    return res
