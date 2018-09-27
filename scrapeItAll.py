from lxml import html
from datetime import datetime
import requests
import sqlite3

def runScraper():
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    res = curs.execute("SELECT * FROM cities") 
    citiesList = []
    for city in res:
        citiesList.append(city[0])
    curs.execute('''DROP TABLE IF EXISTS vehicles''')
    curs.execute('''CREATE TABLE IF NOT EXISTS vehicles(city STRING, price INTEGER, make STRING, condition STRING, cylinders STRING, fuel STRING,
    odometer INTEGER, title_status STRING, transmission STRING, VIN STRING, drive STRING, size STRING, type STRING, paint_color STRING)''')       
    session = requests.Session()  
    scraped = 0
    for city in citiesList:
        print("Scraping vehicles from {}".format(city))  
        empty = False
        while not empty:
            print("Gathering entries {} through {}".format(scraped, scraped + 120))
            page = session.get("https://{}.craigslist.org/d/cars-trucks/search/cta?s={}".format(city, scraped))
            tree = html.fromstring(page.content)
            vehicles = tree.xpath('//a[@class="result-image gallery"]')
            if len(vehicles) == 0:
                empty = True
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
                vehicleDict = {}
                vehicleDict["price"] = int(item[1].strip("$"))
                try:
                    page = session.get(item[0])
                    tree = html.fromstring(page.content)
                except:
                    print("Failed to reach {}, entry has been dropped".format(item[0]))
                    continue
                attrs = tree.xpath('//span//b')
                for item in attrs:
                    try:
                        k = item.getparent().text.strip()
                        k = k.strip(":")
                    except:
                        k = "make"
                    if item == None:
                        continue
                    vehicleDict[k] = item.text.strip()
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
                    if "title_status" in vehicleDict:
                        title_status = vehicleDict["title_status"]    
                    if "transmission" in vehicleDict:
                        transmission = vehicleDict["transmission"]
                    if "VIN" in vehicleDict:
                        VIN = vehicleDict["VIN"]
                    if "drive" in vehicleDict:
                        drive = vehicleDict["drive"]
                    if "size" in vehicleDict:
                        size = vehicleDict["size"]
                    if "vehicle_type" in vehicleDict:
                        vehicle_type = vehicleDict["vehicle_type"]
                    if "paint_color" in vehicleDict:
                        paint_color = vehicleDict["paint_color"]   
                curs.execute('''INSERT INTO vehicles(city, price, make, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, size, type, paint_color)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (city, price, make, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, size, vehicle_type, paint_color))
                scraped += 1
            print("{} vehicles scraped".format(scraped))
            db.commit()
            break
        break
    db.close()      
    
def main():
    runScraper()


if __name__ == "__main__":
    main()