#crawlCities grabs every city on Craigslist

from lxml import html
from requests_html import HTMLSession
import sqlite3

def storeCities():
    #connect to database
    db = sqlite3.connect("cities.db")
    curs = db.cursor()
    curs.execute("DROP TABLE IF EXISTS cities")
    curs.execute("CREATE TABLE IF NOT EXISTS cities(cityURL STRING PRIMARY KEY, cityTitle STRING)")
    
    #create requests session
    s = HTMLSession()
    
    #webpage 'origin' contains all US craigslist regions
    origin = s.get("https://geo.craigslist.org/iso/us/")
    tree = (html.fromstring(origin.content))
    
    #cities = list of elements for each region
    cities = tree.xpath('//ul[@class="height6 geo-site-list"]//li//a')
    
    #major cities are presented in bold text, this must be handled
    boldAt = 0
    for item in cities:
        name = item.text
        #if name == None, text is in bold
        if name == None:
            name = item.xpath("//b")[boldAt].text
            boldAt += 1
            
        #insert url and city name, easy stuff
        curs.execute('''INSERT INTO cities(cityURL, cityTitle) VALUES(?,?)''', (item.attrib["href"], name))
        db.commit()
    db.close()
    
def main():
    storeCities()

if __name__ == "__main__":
    main()