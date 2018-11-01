#this is a work in progress that will grab unique column values to allow for dropdown menus instead of text boxes in the search form

import sqlite3

def queryDropdowns():
    dropdowns = {}
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    curs.execute("SELECT DISTINCT cylinders FROM vehicles")
    cylinders = curs.fetchall()
    curs.execute("SELECT DISTINCT fuel FROM vehicles")
    fuel = curs.fetchall()
    curs.execute("SELECT DISTINCT title_status FROM vehicles")
    titleStatus = curs.fetchall()
    curs.execute("SELECT DISTINCT drive FROM vehicles")
    drive = curs.fetchall()
    curs.execute("SELECT DISTINCT type FROM vehicles")
    vehicleType = curs.fetchall()
    curs.execute("SELECT DISTINCT paint_color FROM vehicles")
    paintColor = curs.fetchall()
    curs.execute("SELECT DISTINCT year FROM vehicles")
    year = curs.fetchall()
    curs.execute("SELECT DISTINCT manufacturer FROM vehicles")
    manufacturer = curs.fetchall()
    curs.execute("SELECT DISTINCT condition FROM vehicles")
    condition = curs.fetchall()
    curs.execute("SELECT DISTINCT size FROM vehicles")
    size = curs.fetchall()
    curs.execute("SELECT DISTINCT transmission FROM vehicles")
    transmission = curs.fetchall()
    db.close()
    transmissions = []    
    for item in transmission:
        item = item[0]
        if item != None:
            transmissions.append((item, item))
    transmissions.append(("", ""))            
    transmissions.sort()
    dropdowns["transmission"] = transmissions        
    sizes = []    
    for item in size:
        item = item[0]
        if item != None:
            sizes.append((item, item))
    sizes.append(("", ""))
    sizes.sort()
    dropdowns["size"] = sizes    
    cyls = []    
    for item in cylinders:
        item = item[0]
        if item != None:
            cyls.append((item, item))
    cyls.append(("", ""))                
    cyls.sort()
    dropdowns["cylinders"] = cyls
    fuels = []    
    for item in fuel:
        item = item[0]
        if item != None:
            fuels.append((item, item))
    fuels.append(("", ""))                
    fuels.sort()
    dropdowns["fuel"] = fuels
    titleStatusList = []    
    for item in titleStatus:
        item = item[0]
        if item != None:
            titleStatusList.append((item, item))
    titleStatusList.append(("", ""))                
    titleStatusList.sort()
    dropdowns["titleStatus"] = titleStatusList
    drives = []    
    for item in drive:
        item = item[0]
        if item != None:
            drives.append((item, item))
    drives.append(("", ""))                    
    drives.sort()
    dropdowns["drive"] = drives
    vehicleTypes = []    
    for item in vehicleType:
        item = item[0]
        if item != None:
            vehicleTypes.append((item, item))
    vehicleTypes.append(("", ""))                        
    vehicleTypes.sort()
    dropdowns["vehicleType"] = vehicleTypes
    paintColors = []    
    for item in paintColor:
        item = item[0]
        if item != None:
            paintColors.append((item, item))
    paintColors.append(("", ""))                        
    paintColors.sort()
    dropdowns["paintColor"] = paintColors
    manufacturers = []    
    for item in manufacturer:
        item = item[0]
        if item != None:
            manufacturers.append((item, item))
    manufacturers.append(("", ""))
    manufacturers.sort()
    refinedManufacturers = []
    dropdowns["manufacturer"] = manufacturers
    years = []    
    for item in year:
        item = item[0]
        if item != None:
            years.append((item, item))
    years.sort()            
    years = [("", "")] + years
    dropdowns["year"] = years
    conditions = []    
    for item in condition:
        item = item[0]
        if item != None:
            conditions.append((item, item))
    conditions.append(("", ""))                        
    conditions.sort()
    dropdowns["condition"] = conditions
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    stateTuples = []
    stateTuples.append(("", ""))
    for item in states:
        stateTuples.append((item, item))
    dropdowns["states"] = stateTuples
    
    return dropdowns
queryDropdowns()


