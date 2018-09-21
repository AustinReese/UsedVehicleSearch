from lxml import html
from datetime import datetime
import requests

def getLocation():
    while True:
        print("Enter a location to search")
        location = input().lower()
        tree = html.fromstring("<html></html>")
        s = 0
        print("How many entries would you like to scrape? (1000 query limit, multiples of 120)")
        target = input()
        try:
            target = int(target)
            if target > 1000:
                print("Your query is too large, requesting 1000 results instead")
                target = 1000
        except:
            print("Your query is not valid, please enter a number")
            continue
        while True:
            session = requests.Session()
            if s > target:
                return tree, location, target
            print("Scraping entries {}-{} from {}.craigslist.org".format(s, s + 120, location))
            try:
                page = session.get("https://{}.craigslist.org/d/cars-trucks/search/cta?s={}".format(location, s))
                s += 120
                tree.append(html.fromstring(page.content))
            except:
                print("Could not reach {}.craiglist.org.".format(location))
                return None, None, None
    
def scrape(tree, target):
    session = requests.Session()
    carsPath = tree.xpath('//a[@class="result-image gallery"]')
    carsList = []
    thrown = 0
    for item in carsPath:
        carDetails = []
        carDetails.append(item.attrib["href"])
        try:
            carDetails.append(item[0].text)
        except:
            thrown += 1
            continue
        carsList.append(carDetails)
    print("Gathered {} entries, {} entries thrown out due to lack of adequate data".format(len(carsList), thrown))
    carsDicts = []
    count = 0
    start = datetime.now()
    for item in carsList:
        count += 1
        if count % 10 == 0:
            print("Building database... {0:.0%} complete".format(round(count / len(carsList), 2)))
        carDict = {}
        carDict["price"] = int(item[1].strip("$"))
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
            carDict[k] = item.text.strip()
        carsDicts.append(carDict)
    done = datetime.now()
    print("{} records logged in {} seconds".format(len(carsDicts), ((done - start).total_seconds())))
    return carsDicts
        
def buildGraph(carsDicts, location):
    miles = []
    prices = []
    for item in carsDicts:
        try:
            miles.append(int(item["odometer"]))
            prices.append(item["price"])
        except:
            continue
    balanced = False
    removed = 0
    while not balanced:
        if max(miles) >= (sum(miles)/len(miles) * 10):
            index = miles.index(max(miles))
            del miles[index]
            del prices[index]
            removed += 1
        elif max(prices) >= (sum(prices)/len(prices) * 10):
            index = prices.index(max(prices))
            del miles[index]
            del prices[index]            
            removed += 1
        else:
            balanced = True
    print("{} outliers removed".format(removed))
        

    now = datetime.now()
    
    fileName = str(now).replace(" ", ":") + "-{}-{}EntriesLogged.xml".format(location, len(miles))
    file = open(fileName, "w")
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    file.write('<Plot title="Vehicle Prices vs Miles Driven in {}">\n'.format(location.title()))
    file.write('  <Axes>\n')
    file.write('    <XAxis min="'+str(0)+'" max="'+str(max(miles))+'">Miles Driven</XAxis>\n')
    file.write('    <YAxis min="'+str(0)+'" max="'+str(max(prices))+'">Vehicle Price in US Dollars</YAxis>\n')
    file.write('  </Axes>\n')
    file.write('  <Sequence title="Vehicle Price vs Miles Driven in {}" color="blue">\n'.format(location.title()))         
  
    for i in range(len(miles)):
        file.write('    <DataPoint x="'+str(miles[i])+'" y="'+str(prices[i])+'"/>\n')
        
    file.write('  </Sequence>\n')
    file.write('</Plot>\n')    
    file.close()
    print("{} written successfully".format(fileName))

def main():
    remain = True
    while remain:
        tree, location, target = getLocation()
        if tree is not None:
            carsDicts = scrape(tree, target)
            buildGraph(carsDicts, location)
        print("Press enter to try a new search, enter EXIT to terminate the program")
        remainPrompt = input()
        if remainPrompt.upper() == "EXIT":
            print("Goodbye")
            remain = False

if __name__ == "__main__":
    main()