import sqlite3

def query(data):
    city = data.city.data
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
    odom = data.odometer.data
        
    criteriaDict = {city: "city", make: "make", cond: "condiiton", 
                    cyl: "cylinders", tran: "transmission", vin: "vin",
                    drive: "drive", size: "size", vType: "vehicleType", 
                    color: "paintColor", price: "price", odom: "odometer"}
    
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
