# scrapeVehicles.py loops through all cities listed on Craigslist and scrapes every vehicle for sale and adds it to cities.db
# this program will take awhile to run, don't run unless you're willing to let it sit for at least 2 hours
# the database is commited after we've finished scraping each city, so the program can be terminated and results are still saved if you need to exit for any reason

import os
import psycopg2
from json import loads
from lxml import html
from datetime import datetime
from requests_html import HTMLSession
from connect import connect
from crawlCities import storeCities

import sys,os
sys.path.append(os.getcwd())

def runScraper():
    storeCities()
    
    conn = connect()
    
    #the cities table contains around 480 cities, all of the craigslist pages in north america
    
    curs = conn.cursor()
    curs.execute("SELECT * FROM cities")
    
    citiesList = []
    for city in curs.fetchall():
        citiesList.append(city)
    
    curs = conn.cursor()
            
    curs.execute('''
    CREATE TABLE IF NOT EXISTS housing(
    id BIGINT PRIMARY KEY NOT NULL,
    url TEXT NOT NULL,
    region TEXT NOT NULL,
    region_url TEXT NOT NULL,
    price BIGINT NOT NULL,
    type TEXT NOT NULL,
    sqfeet TEXT NOT NULL,
    beds REAL NOT NULL,
    baths REAL NOT NULL,
    cats_allowed INT NOT NULL,
    dogs_allowed INT NOT NULL,
    smoking_allowed INT NOT NULL,
    wheelchair_access INT NOT NULL,
    electric_vehicle_charge INT NOT NULL,
    comes_furnished INT NOT NULL,
    laundry_options TEXT,
    parking_options TEXT,
    image_url TEXT, 
    description TEXT,
    lat REAL,
    long REAL,
    state TEXT
    )''') 
        
    session = HTMLSession()
    
    #scraped counts all entries gathered
    scraped = 0
    
    #simple txt file mechanism to track scraping progress
    fileName = os.path.dirname(os.path.abspath(__file__)) + "/static/trackHousingScraping.txt"
    exists = os.path.isfile(fileName)
    if not exists:
        tracker = open(fileName, "w")
        tracker.write("0")
        tracker.close()
    
    with open(fileName, "r") as tracker:
        cities = int(tracker.readlines()[0])
    citiesCount = len(citiesList)
    citiesList = citiesList[cities:]
    
    housingOptions = {
        "apartment",
        "condo",
        "cottage/cabin",
        "duplex",
        "flat",
        "house",
        "in-law",
        "loft",
        "townhouse",
        "manufactured",
        "assisted living",
        "land"
    }
    
    laundryOptions = {
        "w/d in unit",
        "w/d hookups",
        "laundry in bldg",
        "laundry on site",
        "no laundry on site"
    }
    
    parkingOptions = {
        "carport",
        "attached garage",
        "detached garage",
        "off-street parking",
        "street parking",
        "valet parking",
        "no parking"
    }
    
    for city in citiesList:
        scrapedInCity = 0
        cities += 1
        print(f"Scraping housing from {city[1]}, {citiesCount - cities} cities remain")
        empty = False
        
        #scrapedIds is used to store each individual vehicle id from a city, therefore we can delete vehicle records from the database
        #if their id is no longer in scrapedIds under the assumption that the entry has been removed from craigslist
        scrapedIds = set([])
        
        #track items skipped that are already in the database
        skipped = 0
        
        #this loop executes until we are out of search results, craigslist sets this limit at 3000 and cities often contain the full 3000 records (but not always)        
        while not empty:
            print(f"Gathering entries {scrapedInCity} through {scrapedInCity + 120}")
            
            #now we scrape
            try:
                searchUrl = f"{city[1]}/d/apts-housing-for-rent/search/apa?s={scrapedInCity}"
                page = session.get(searchUrl)
            except Exception as e:
                #catch any excpetion and continue the loop if we cannot access a site for whatever reason
                print(f"Failed to reach {searchUrl}, entries have been dropped: {e}")
                continue
            
            #each search page contains 120 entries
            scrapedInCity += 120
            tree = html.fromstring(page.content)
            
            #the following line returns a list of urls for different housing options
            housingElement = tree.xpath('//a[@class="result-image gallery"]')
            if len(housingElement) == 0:
                #if we no longer have entries, continue to the next city
                empty = True
                continue
            housingList = []
            for item in housingElement:
                housingDetails = []
                housingDetails.append(item.attrib["href"])
                try:
                    #this code attempts to grab the price of the housing options. some housing options dont have prices (which throws an exception)
                    #and we dont want those which is why we toss them
                    housingDetails.append(item[0].text.strip("$"))
                except:
                    continue
                housingList.append(housingDetails)
            
            #loop through each vehicle
            for item in housingList:
                url = item[0]
                price = item[1]
                try:
                    idpk = int(url.split("/")[-1].strip(".html"))
                except ValueError as e:
                    print("{} does not have a valid id: {}".format(url, e))
                
                #add the id to scrapedIds for database cleaning purposes
                scrapedIds.add(idpk)
                
                #housing id is a primary key in this database so we cant have repeats. if a record with the same url is found, we continue
                #the loop as the housing option has already been stored
                
                curs.execute(f"SELECT 1 FROM housing WHERE id = {idpk}")
                if len(curs.fetchall()) != 0:
                    skipped += 1
                    continue
                
                housingDict = {}
                housingDict["price"] = int(item[1])
                
                try:
                    #grab each individual vehicle page
                    page = session.get(url)
                    tree = html.fromstring(page.content)
                except:
                    print(f"Failed to reach {url}, entry has been dropped")
                    continue
                
                baseAttrs = tree.xpath("//p[@class='attrgroup']//span//b")
                baseAttrs = [i.text for i in baseAttrs]
                
                #we require that all entries have number of beds, baths, and square footage. if one of these is missing we skip.
                if len(baseAttrs) < 3:
                    continue
                                
                optionalAttrs = tree.xpath("//p[@class='attrgroup']//span")[len(baseAttrs) - 1:]
                
                #'\n                        ' is a bad character associated with open viewing days which we don't care about
                optionalAttrs = set([i.text for i in optionalAttrs if i != '\n                        '])
                
                #while optional attrs include many boolean values which are not required, we need at least 1 option that matches
                #a valid housing type. however we may as well check if set is empty first to minimize set operations
                
                if len(optionalAttrs) == 0:
                    continue
                
                if housingOptions.isdisjoint(optionalAttrs) == True:
                    #no crossover in valid housing types, skip
                    continue
                else:
                    typeSet = housingOptions.intersection(optionalAttrs)
                    if len(typeSet) != 1:
                        print("url {} has multiple housing types {}".format(url, typeSet))
                    else:
                        housingType = typeSet.pop()               
                
                try:
                    beds = float(baseAttrs[0].lower().strip("br"))
                except ValueError:
                    continue

                try:
                    baths = float(baseAttrs[1].lower().strip("ba"))
                except ValueError:
                    continue
                
                try:
                    sqfeet = int(baseAttrs[2])
                except ValueError:
                    continue
                
                #default optional attributes to None or the default value unless otherwise specified by the listing
                
                img_url = None
                lat = None
                long = None
                description = None
                cats = 0
                dogs = 0
                smoking = 1
                wheelchair = 0
                electricCharge = 0
                furnished = 0
                laundry = None
                parking = None
                
                #proceed with optional laundry and parking options if exist
                
                if laundryOptions.isdisjoint(optionalAttrs) == False:
                    laundrySet = laundryOptions.intersection(optionalAttrs)
                    if len(laundrySet) != 1:
                        print("url {} has multiple housing types {}".format(url, laundrySet))
                    else:
                        laundry = laundrySet.pop()
                        
                if parkingOptions.isdisjoint(optionalAttrs) == False:
                    parkingSet = parkingOptions.intersection(optionalAttrs)
                    if len(parkingSet) != 1:
                        print("url {} has multiple housing types {}".format(url, parkingSet))
                    else:
                        parking = parkingSet.pop()
                
                #set booleans accordingly
                if "cats are OK - purrr" in optionalAttrs:
                    cats = 1
                if "dogs are OK - wooof" in optionalAttrs:
                    dogs = 1
                if "furnished" in optionalAttrs:
                    furnished = 1
                if "no smoking" in optionalAttrs:
                    smoking = 0
                if "wheelchair accessible" in optionalAttrs:
                    wheelchair = 1
                if "EV charging" in optionalAttrs:
                    electricCharge = 1
                
                #now lets fetch the image url if exists
                
                try:
                    img = tree.xpath('//div[@class="slide first visible"]//img')
                    img_url = img[0].attrib["src"]
                except:
                    pass
                
                #try to fetch lat/long, remain as None if they do not exist
                
                try:
                    location = tree.xpath("//div[@id='map']")
                    lat = float(location[0].attrib["data-latitude"])
                    long = float(location[0].attrib["data-longitude"])
                except:
                    pass
                
                #try to fetch housing description, remain as None if it does not exist
                
                try:
                    location = tree.xpath("//section[@id='postingbody']")
                    description = location[0].text_content().replace("\n", " ").replace("QR Code Link to This Post", "").strip()
                except:
                    pass

                #finally we get to insert the entry into the database

                curs.execute('''
                INSERT INTO housing(
                id, url, region, region_url, price, type, sqfeet, beds, baths, cats_allowed, dogs_allowed,
                smoking_allowed, wheelchair_access, electric_vehicle_charge,
                comes_furnished, laundry_options, parking_options, image_url, description, lat, long, state) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (idpk, url, city[1], city[0], price, housingType, sqfeet, beds, baths, cats, dogs, smoking,
                     wheelchair, electricCharge, furnished, laundry, parking, img_url, description, lat, long, city[3]))

                scraped += 1

            #these lines will execute every time we grab a new page (after 120 entries)
            print("{} housing options scraped".format(scraped))

        
        #now to clean the database we grab all urls from the city that are already logged
        curs.execute("SELECT id FROM housing WHERE region_url = '{}'".format(city[0]))
        deleted = 0
        
        #if a given id is not in scrapedIds (the ids that we just scraped) then the entry no longer exists and we remove it
        for oldId in curs.fetchall():
            if int(oldId[0]) not in scrapedIds:
                curs.execute("DELETE FROM housing WHERE id = '{}'".format(oldId[0]))
                deleted += 1
        print("Deleted {} old records, {} records skipped as they are already stored".format(deleted, skipped))
        conn.commit()
        
        #update progress file
        with open(fileName, "w") as tracker:
            tracker.write(str(cities))
        
    #delete tracker file
    os.remove(fileName)
    count = curs.execute("SELECT Count(*) FROM housing")
    print("Table housing successfully updated, {} entries exist".format(\
        curs.fetchall()[0][0]))
    conn.close()
    
def main():
    runScraper()


if __name__ == "__main__":
    main()
