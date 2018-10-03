import sqlite3

def queryForm(data):
    city = data.city.data
    manu = data.manufacturer.data
    make = data.make.data
    cond = data.condition.data
    cyl = data.cylinders.data
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
        
    criteriaDict = {city: "city", manu: "manufacturer", make: "make", cond: "condiiton", 
                    cyl: "cylinders", tran: "transmission", vin: "vin",
                    drive: "drive", size: "size", vType: "vehicleType", 
                    color: "paintColor", price: "price", year: "year", odom: "odometer"}
    
    whereClause = ""
    for k, v in criteriaDict.items():
        if k:
            whereClause = whereClause + "{} LIKE '{}' AND ".format(v, k)
    
    whereClause = whereClause[:-5]
        
    query = "SELECT * FROM vehicles WHERE {} LIMIT 100;".format(whereClause)
    
    print(query)
    
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    curs.execute(query)
    res = curs.fetchall()
    db.close()
        
    return res
