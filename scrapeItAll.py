from lxml import html
from datetime import datetime
import requests
import sqlite3
from random import shuffle

def runScraper():
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    res = curs.execute("SELECT * FROM cities") 
    citiesList = []
    for city in res:
        citiesList.append(city[0])
    curs.execute('''CREATE TABLE IF NOT EXISTS vehicles(url STRING PRIMARY KEY, city STRING, price INTEGER, make STRING, condition STRING, cylinders STRING, fuel STRING,
    odometer INTEGER, title_status STRING, transmission STRING, VIN STRING, drive STRING, size STRING, type STRING, paint_color STRING)''')       
    session = requests.Session()  
    scraped = 0
    cities = 0
    shuffle(citiesList)
    for city in citiesList:
        scrapedInCity = 0
        cities += 1
        print("Scraping vehicles from {}, {} cities remain".format(city, len(citiesList) - cities))
        empty = False
        townUrls = []        
        while not empty:
            print("Gathering entries {} through {}".format(scrapedInCity, scrapedInCity + 120))
            page = session.get("https://{}.craigslist.org/d/cars-trucks/search/cta?s={}".format(city, scrapedInCity))
            scrapedInCity += 120
            tree = html.fromstring(page.content)
            vehicles = tree.xpath('//a[@class="result-image gallery"]')
            if len(vehicles) == 0:
                empty = True
                print("All done in {}, moving along...".format(city))
                continue
            vehiclesList = []
            thrown = 0
            for item in vehicles:
                vehicleDetails = []
                vehicleDetails.append(item.attrib["href"])
                try:
                    vehicleDetails.append(item[0].text)
                except:
                    thrown += 1
                    continue
                vehiclesList.append(vehicleDetails)
            print("{} entries tossed".format(thrown))
            for item in vehiclesList:
                url = item[0]
                townUrls.append(url)
                vehicleDict = {}
                vehicleDict["price"] = int(item[1].strip("$"))
                curs.execute("SELECT 1 FROM vehicles WHERE url ='{}'".format(url))
                if curs.fetchall():
                    continue
                try:
                    page = session.get(url)
                    tree = html.fromstring(page.content)
                except:
                    print("Failed to reach {}, entry has been dropped".format(url))
                    continue
                attrs = tree.xpath('//span//b')
                for item in attrs:
                    try:
                        k = item.getparent().text.strip()
                        k = k.strip(":")
                    except:
                        k = "make"
                    try:
                        vehicleDict[k] = item.text.strip()
                    except:
                        continue
                for item in vehicleDict:
                    price = None
                    make = None
                    condition = None
                    cylinders = None
                    fuel = None
                    odometer = None
                    title_status = None
                    transmission = None
                    VIN = None
                    drive = None
                    size = None
                    vehicle_type = None
                    paint_color = None
                    if "price" in vehicleDict:
                        try:
                            price = int(vehicleDict["price"])
                        except Exception as e:
                            print("Could not parse price: {}".format(e))
                    if "odomoter" in vehicleDict:
                        try:
                            odometer = int(vehicleDict["odometer"])
                        except Exception as e:
                            print("Could not parse odometer: {}".format(e))
                    if "condition" in vehicleDict:
                        condition = vehicleDict["condition"]
                    if "make" in vehicleDict:
                        make = vehicleDict["make"]
                    if "cylinders" in vehicleDict:
                        cylinders = vehicleDict["cylinders"]
                    if "fuel" in vehicleDict:
                        fuel = vehicleDict["fuel"]
                    if "odometer" in vehicleDict:
                        odometer = vehicleDict["odometer"]
                    if "title status" in vehicleDict:
                        title_status = vehicleDict["title status"]    
                    if "transmission" in vehicleDict:
                        transmission = vehicleDict["transmission"]
                    if "VIN" in vehicleDict:
                        VIN = vehicleDict["VIN"]
                    if "drive" in vehicleDict:
                        drive = vehicleDict["drive"]
                    if "size" in vehicleDict:
                        size = vehicleDict["size"]
                    if "type" in vehicleDict:
                        vehicle_type = vehicleDict["type"]
                    if "paint color" in vehicleDict:
                        paint_color = vehicleDict["paint color"]   
                curs.execute('''INSERT INTO vehicles(url, city, price, make, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, size, type, paint_color)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (url, city, price, make, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, size, vehicle_type, paint_color))
                scraped += 1
                if len(vehicleDict) > 13:
                    print("-------------------------ALERT-------------------------------")
                    print(len(vehicleDict))
                    print(vehicleDict)
            print("{} vehicles scraped".format(scraped))
            db.commit()
        curs.execute("SELECT url FROM vehicles WHERE city = '{}'".format(city))
        deleted = 0
        for cityUrl in curs:
            if cityUrl[0] not in townUrls:
                curs.execute("DELETE FROM vehicles WHERE url = '{}'".format(cityUrl[0]))
                deleted += 1
        print("Deleted {} old records".format(deleted))
    print("vehicles.db successfully updated, {} entries exist".format(curs.rowcount))
    db.close()      
    
def main():
    runScraper()


if __name__ == "__main__":
    main()