#this is a work in progress that will grab unique column values to allow for dropdown menus instead of text boxes in the search form

import psycopg2
from connect import connect

def queryDropdowns():
    dropdowns = {}
    cylinders = [('4 cylinders',), (None,), ('10 cylinders',), ('8 cylinders',), ('6 cylinders',), ('5 cylinders',), ('3 cylinders',), ('other',), ('12 cylinders',)]
    fuel = [(None,), ('other',), ('hybrid',), ('gas',), ('diesel',), ('electric',)]
    titleStatus = [(None,), ('salvage',), ('parts only',), ('missing',), ('lien',), ('clean',), ('rebuilt',)]
    drive = [(None,), ('rwd',), ('fwd',), ('4wd',)]
    vehicleType = [(None,), ('wagon',), ('sedan',), ('SUV',), ('bus',), ('truck',), ('mini-van',), ('convertible',), ('pickup',), ('hatchback',), ('other',), ('offroad',), ('coupe',), ('van',)]
    paintColor = [('purple',), ('orange',), ('green',), ('blue',), ('brown',), ('grey',), ('yellow',), ('black',), ('white',), ('red',), (None,), ('silver',), ('custom',)]
    year = [(2000,), (2011,), (1948,), (1965,), (1932,), (1985,), (1949,), (1941,), (1947,), (1938,), (1925,), (1906,), (1918,), (1946,), (1960,), (1951,), (1976,), (1972,), (1998,), (1915,), (1966,), (1981,), (2007,), (1916,), (1927,), (1978,), (1929,), (1944,), (1968,), (2006,), (1961,), (1952,), (2020,), (1962,), (2001,), (1926,), (1950,), (1999,), (1937,), (1923,), (1957,), (1955,), (1900,), (2012,), (1954,), (1959,), (1988,), (1964,), (2021,), (1969,), (None,), (2008,), (1989,), (1991,), (0,), (1945,), (1974,), (1943,), (1935,), (1971,), (1977,), (1940,), (1956,), (1984,), (1983,), (2017,), (1934,), (2009,), (1958,), (2005,), (1973,), (2013,), (1914,), (1933,), (2003,), (2015,), (1930,), (1990,), (1993,), (1903,), (1953,), (2002,), (1979,), (1997,), (2004,), (1980,), (1919,), (2016,), (1921,), (1936,), (1975,), (1970,), (1986,), (2018,), (1982,), (1942,), (1995,), (1992,), (1920,), (1963,), (1994,), (1928,), (2014,), (2010,), (1924,), (1939,), (2019,), (1931,), (1996,), (1987,), (1967,)]
    manufacturer = [(None,), ('chevrolet',), ('mazda',), ('acura',), ('audi',), ('nissan',), ('mini',), ('mercedes-benz',), ('chrysler',), ('ram',), ('kia',), ('pontiac',), ('bmw',), ('hennessey',), ('infiniti',), ('volkswagen',), ('morgan',), ('ford',), ('harley-davidson',), ('jaguar',), ('fiat',), ('hyundai',), ('volvo',), ('gmc',), ('rover',), ('alfa-romeo',), ('honda',), ('mercury',), ('aston-martin',), ('buick',), ('lexus',), ('tesla',), ('toyota',), ('saturn',), ('land rover',), ('mitsubishi',), ('cadillac',), ('subaru',), ('lincoln',), ('jeep',), ('porche',), ('datsun',), ('ferrari',), ('dodge',)]
    condition = [('excellent',), ('new',), ('good',), ('fair',), (None,), ('salvage',), ('like new',)]
    size = [('sub-compact',), (None,), ('mid-size',), ('compact',), ('full-size',)]
    transmission = [(None,), ('other',), ('manual',), ('automatic',)]
    
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
    
    sortByList = ["Price low to high", "Price high to low", "Odometer low to high", "Odometer high to low", "Year low to high", "Year high to low"]
    sortByTuples = []
    sortByTuples.append(("", ""))
    for item in sortByList:
        sortByTuples.append((item, item))
    dropdowns["sortBy"] = sortByTuples
    
    return dropdowns



