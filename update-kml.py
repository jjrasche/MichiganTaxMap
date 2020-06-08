import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, element
from collections import OrderedDict  

class Placemark:
    def __init__(self, arg):
        if isinstance(arg, element.Tag):
            self.county = arg.find("data", {"name":"County"}).text
            self.locality = arg.find("data", {"name":"Locality"}).text
            self.schoolDistrict = arg.find("data", {"name":"School District"}).text
            self.primary = arg.find("data", {"name":"primary"}).text
            self.secondary = arg.find("data", {"name":"secondary"}).text
        elif isinstance(arg, list):
            self.county = arg[0]
            self.locality = arg[1]
            self.schoolDistrict = arg[2]
            self.primary = arg[3]
            self.secondary = arg[4]
        else:
            raise Exception("Placemark object not of valid type")
    def __eq__(self, other): 
        if not isinstance(other, Placemark):
            # don't attempt to compare against unrelated types
            return NotImplemented
        if (self.county == other.county and
            self.locality == other.locality and
            self.schoolDistrict == other.schoolDistrict and
            self.primary == other.primary and
            self.secondary == other.secondary):
            return True
        else:
            return False

def extractPlacemarksFromKML(fileName):
    placemarkObjects = []
    with open(fileName) as f:
        kmlData = f.read()
        xml = BeautifulSoup(kmlData)
        placemarks = xml.findAll("placemark")
        for placemarkTag in placemarks:
            placemarkObjects.append(Placemark(placemarkTag))
    return placemarkObjects


def extractMillagesFromCSV(fileName):
    placemarkObjects = []
    with open(fileName) as f:
        content = f.read().split("\n")
        for line in content:
            cells = list(map(lambda c: c.strip(), line.split(",")))
            try:
                placemarkObjects.append(Placemark(cells))
            except Exception as e:
                print(e)
    return placemarkObjects

# def group_list(lst):
#     res =  [(el.county + el.locality + el.schoolDistrict) for el in lst] 
#     return list(OrderedDict(res).items())


# fileName = "./kml-data2018/schools_locales_modified.kml"
currentPlacemarks = extractPlacemarksFromKML("./kml-data2018/schools_locales_modified.kml")
newPlaceMarks = extractMillagesFromCSV("./county-locale-school-millage-2017-2018.csv")

l1 = list([1,2,3,4,5])
l2 = list([4,5])

matching = [a for a in l1 if a in l2]

matching = [cp for cp in currentPlacemarks if cp in newPlaceMarks]
# nameList = list(map(lambda p: p.county + p.locality + p.schoolDistrict, currentPlacemarks))
# unique = set(nameList)
test = 5


