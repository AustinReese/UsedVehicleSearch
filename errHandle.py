#confirm the necessary tables exist to run this app

import sqlite3

def errHandle():
    try:
        db = sqlite3.connect("cities.db")
        curs = db.cursor()
        curs.execute("SELECT 1 FROM vehicles LIMIT 1")
        db.close()
    except:
        raise EnvironmentError("Please run both crawlCities.py and scrapeVehicles.py")