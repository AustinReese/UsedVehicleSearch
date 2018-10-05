#crawlCities grabs every city on Craigslist

from lxml import html
from datetime import datetime
import requests
import sqlite3

db = sqlite3.connect("cities.db")
curs = db.cursor()
curs.execute("DROP TABLE IF EXISTS cities")
curs.execute("CREATE TABLE IF NOT EXISTS cities(cityId STRING PRIMARY KEY, cityTitle STRING)")

s = requests.Session()

def cityLooper(baseCase):
    start = datetime.now()
    try:
        origin = s.get("https://{}.craigslist.com".format(baseCase))
    except:
        print("Could not reach {}.craigslist.com, is this link broken?".format(baseCase))
        return None
    
    tree = (html.fromstring(origin.content))
    #so each city page on Craigslist has a recommeded cities page, essentially we grab each recommended city from the current city
    #and store them in the cityQueue (which is a set so we cant have duplicates)
    cityQueue = set(tree.xpath('//li[@class="s"]//a'))
    crawled = set()
    newEntry = True
    
    while len(cityQueue) != 0:
        city = cityQueue.pop()
        moreCities, crawled, updated = cityCrawler(city, crawled)
        if updated:
            cityQueue.update(moreCities)
            #difference_update will remove entries from cityQueue if the same entry is already in crawled
            cityQueue.difference_update(crawled)
            print("Added {}. {} regions crawled through, {} regions in the queue.".format(city.text.title(), len(crawled), len(cityQueue)))
    db.commit()
    db.close()    
    end = datetime.now()
    print("Program complete. Run time: {} seconds. File cities.db contains entries for {} regions on craigslist.com".format(int((end - start).total_seconds()), len(crawled)))
        
def cityCrawler(city, crawled):
    cityCode = city.attrib["href"][2:city.attrib["href"].index(".")]
    
    if cityCode in crawled:
        #this means we've already checked it out, no need to execute anything
        return set(), crawled, False
    else:
        #otherwise put the city in the db and fetch the 'recommended cities' from the current target
        curs.execute("INSERT INTO cities(cityId, cityTitle) VALUES(?,?)", (cityCode, city.text))
        
        try:
            newOrigin = s.get("https://{}.craigslist.com".format(cityCode))
        except:
            print("Could not reach {}.craigslist.com, is this link broken?".format(baseCase))
            return set(), crawled, False
    
    crawled.add(cityCode)
    tree = (html.fromstring(newOrigin.content))
    newCities = set(tree.xpath('//li[@class="s"]//a'))
    #newCities is a set of the recommended cities featured on the current city
    return newCities, crawled, True
    

def main():
    cityLooper("kansascity")
    
if __name__ == "__main__":
    main()