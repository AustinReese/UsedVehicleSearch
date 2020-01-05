#crawlCities grabs every city on Craigslist

import psycopg2
import re
from lxml import html
from requests_html import HTMLSession
from connect import connect

def storeCities():
    conn = connect()

    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS cities")

    curs.execute("CREATE TABLE IF NOT EXISTS cities(citystate TEXT PRIMARY KEY, cityURL TEXT , cityTitle TEXT, stateCode TEXT)")
    
    # stateCodes
    states = ["al","ak","az","ar","ca","co","ct","dc","de","fl","ga","hi","id","il","in","ia","ks","ky","la","me","md","ma","mi","mn","ms","mo","mt","nc","ne","nv","nj","nm","ny","nh","nd","oh","ok","or","pa","ri","sc","sd","tn","tx","ut","vt","va","wa","wv","wi","wy"]

    #create requests session
    s = HTMLSession()
    
    print("scraping regions")
    
    for state in states:
        url = "https://geo.craigslist.org/iso/us/"+state
        print("Fetching from "+url)
        origin = s.get(url)
        tree = (html.fromstring(origin.content))
        #cities = list of elements for each region
        cities = tree.xpath('//ul[contains(concat( " " , @class, " "), " geo-site-list ")]//li//a')
        #major cities are presented in bold text, this must be handled
        boldAt = 0
        for item in cities:
            name = item.text
            #if name == None, text is in bold
            if name == None:
                name = item.xpath("//b")[boldAt].text
                boldAt += 1
            if not re.match(r"[a-z]*, [A-Z]*", name):
                #insert url and city name, easy stuff
                link = item.attrib['href']
                if link[:4] != "http":
                    continue
                curs.execute(f'''INSERT INTO cities VALUES('{name.replace("'", "''")+state}','{link}', '{name.replace("'", "''")}', '{state}')''')
                
    conn.commit()
    count = curs.execute("SELECT Count(*) FROM cities")
    print("{} regions added to database".format(curs.fetchall()[0][0]))
    conn.close()
    
def main():
    storeCities()

if __name__ == "__main__":
    main()