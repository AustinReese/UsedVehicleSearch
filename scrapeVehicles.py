# scrapeVehicles.py loops through all cities listed on Craigslist and scrapes every vehicle for sale and adds it to cities.db
# this program will take awhile to run, don't run unless you're willing to let it sit for at least 2 hours
# the database is commited after we've finished scraping each city, so the program can be terminated and results are still saved if you need to exit for any reason

from lxml import html
from datetime import datetime
from random import shuffle
from requests_html import HTMLSession
import sqlite3

def runScraper():
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    
    #the cities table contains around 480 cities, all of the craigslist pages in north america. the table can be generated by running crawlCities.py
    res = curs.execute("SELECT * FROM cities")
    citiesList = []
    for city in res:
        citiesList.append(city[0])
    
    curs.execute('''CREATE TABLE IF NOT EXISTS vehicles(url STRING PRIMARY KEY, city STRING, price INTEGER, year INTEGER, manufacturer STRING,
    make STRING, condition STRING, cylinders STRING, fuel STRING, odometer INTEGER, title_status STRING, transmission STRING, VIN STRING,
    drive STRING, size STRING, type STRING, paint_color STRING, image_url STRING, lat FLOAT, long FLOAT)''')
    session = HTMLSession()
    
    #scraped counts all entries gathered, cities counts cities looped through
    scraped = 0
    cities = 0
    
    #list is shuffled so that we don't loop through the same cities in the same order each time
    shuffle(citiesList)
    
    #carBrands dictate what qualifies as a brand so we can snatch that data from the 'make' tag
    carBrands = ["ford", "toyota", "chevrolet", "chev", "chevy", "honda", "jeep", "hyundai", "subaru",
                 "kia", "gmc", "ram", "dodge", "mercedes-benz", "mercedes", "mercedesbenz",
                 "volkswagen", "vw", "bmw", "saturn", "land rover", "landrover", "pontiac", 
                 "mitsubishi", "lincoln", "volvo", "mercury", "harley-davidson", "harley", 
                 "rover", "buick", "cadillac", "infiniti", "infinity", "audi", "mazda", "chrysler",
                 "acura", "lexus", "nissan", "datsun", "jaguar", "alfa", "alfa-romeo", "aston", "aston-martin",
                 "ferrari", "fiat", "hennessey", "porche", "noble", "morgan", "mini"]
    
    #if the car year is beyond next year, we toss it out. this variable is used later
    nextYear = datetime.now().year + 1
    
    for city in citiesList:
        scrapedInCity = 0
        cities += 1
        print("Scraping vehicles from {}, {} cities remain".format(city, len(citiesList) - cities))
        empty = False
        
        #townUrls is used to store each individual vehicle url from a city, therefore we can delete vehicle records from the database
        #if their url is no longer in townUrls under the assumption that the entry has been removed from craigslist
        townUrls = set([]) 
        
        #this loop executes until we are out of search results, craigslist sets this limit at 3000 and cities often contain the full 3000 records (but not always)
        while not empty:
            print("Gathering entries {} through {}".format(scrapedInCity, scrapedInCity + 120))
            
            #now we scrape
            try:
                searchUrl = "https://{}.craigslist.org/d/cars-trucks/search/cta?s={}".format(city, scrapedInCity)
                page = session.get(searchUrl)
            except:
                #catch any excpetion and continue the loop if we cannot access a site for whatever reason
                print("Failed to reach {}, entry has been dropped".format(searchUrl))
                continue
            
            #each search page contains 120 entries
            scrapedInCity += 120
            tree = html.fromstring(page.content)
            
            #the following line returns a list of urls for different vehicles
            vehicles = tree.xpath('//a[@class="result-image gallery"]')
            if len(vehicles) == 0:
                #if we no longer have entries, continue to the next city
                empty = True
                print("All done in {}, moving along...".format(city))
                continue
            vehiclesList = []
            thrown = 0
            for item in vehicles:
                vehicleDetails = []
                vehicleDetails.append(item.attrib["href"])
                try:
                    #this code attempts to grab the price of the vehicle. some vehicles dont have prices (which throws an exception)
                    #and we dont want those which is why we toss them
                    vehicleDetails.append(item[0].text)
                except:
                    thrown += 1
                    continue
                vehiclesList.append(vehicleDetails)
            print("{} entries tossed due to inadequate data".format(thrown))
            
            #loop through each vehicle
            for item in vehiclesList:
                url = item[0]
                
                #add the url to townUrls for database cleaning purposes
                townUrls.add(url)
                vehicleDict = {}
                vehicleDict["price"] = int(item[1].strip("$"))
                
                #vehicle url is a primary key in this database so we cant have repeats. if a record with the same url is found, we continue
                #the loop as the vehicle has already been stored
                curs.execute("SELECT 1 FROM vehicles WHERE url ='{}'".format(url))
                if curs.fetchall():
                    continue
                try:
                    #grab each individual vehicle page
                    page = session.get(url)
                    tree = html.fromstring(page.content)
                except:
                    print("Failed to reach {}, entry has been dropped".format(url))
                    continue
                
                attrs = tree.xpath('//span//b')
                #this fetches a list of attributes about a given vehicle. each vehicle does not have every specific attribute listed on craigslist
                #so this code gets a little messy as we need to handle errors if a car does not have the attribute we're looking for
                for item in attrs:
                    try:
                        #make is the only attribute without a specific tag on craigslist, so if this code fails it means that we've grabbed the make of the vehicle
                        k = item.getparent().text.strip()
                        k = k.strip(":")
                    except:
                        k = "make"
                    try:
                        #this code fails if item=None so we have to handle it appropriately
                        vehicleDict[k] = item.text.strip()
                    except:
                        continue
                    
                #we will assume that each of these variables are None until we hear otherwise
                #that way, try/except clauses can simply pass and leave these values as None
                price = None
                year = None
                manufacturer = None
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
                image_url = None
                lat = None
                long = None
                
                #now this code gets redundant. if we picked up a specific attr in the vehicleDict then we can change the variable from None.
                #integer attributes (price/odometer) are handled in case the int() is unsuccessful, but i have never seen that be the case
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
                    #make actually contains 3 variables that we'd like: year, manufacturer, and model (which we call make)
                    try:
                        year = int(vehicleDict["make"][:4])
                        if year > nextYear:
                            year = None
                    except:
                        year = None
                    make = vehicleDict["make"][5:]
                    foundManufacturer = False
                    #we parse through each word in the description and search for a match with carBrands (at the top of the program)
                    #if a match is found then we have our manufacturer, otherwise we set make to the entire string and leave manu blank
                    for word in make.split():
                        if word.lower() in carBrands:
                            foundManufacturer = True
                            make = ""
                            manufacturer = word.lower()
                            continue
                        if foundManufacturer:
                            make = make + word.lower() + " "
                    make = make.strip()
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
                    
                #now lets fetch the image url, latitude, and longitude if they exist
                
                try:
                    img = tree.xpath('//div[@class="slide first visible"]//img')
                    image_url = img[0].attrib["src"]
                except:
                    pass
                
                try:
                    location = tree.xpath("//div[@id='map']")
                    lat = float(location[0].attrib["data-latitude"])
                    long = float(location[0].attrib["data-longitude"])
                except:
                    pass
                
                #finally we get to insert the entry into the database
                curs.execute('''INSERT INTO vehicles(url, city, price, year, manufacturer, make, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, size, type, 
                paint_color, image_url, lat, long)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (url, city, price, year, manufacturer, make, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, 
                                                                     size, vehicle_type, paint_color, image_url, lat, long))
                scraped += 1
            #these lines will execute every time we grab a new page (after 120 entries)
            print("{} vehicles scraped".format(scraped))
            db.commit()
        
        #now to clean the database we grab all urls from the city that are already logged
        curs.execute("SELECT url FROM vehicles WHERE city = '{}'".format(city))
        deleted = 0
        
        #if a given url is not in townUrls (the urls that we just scraped) then the entry no longer exists and we remove it
        for cityUrl in curs.fetchall():
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