import csv
import sys
from fuzzywuzzy import fuzz
csv.field_size_limit(sys.maxsize)

headers = [
    "geometry",
    "geometry_vertex_count",
    "County",
    "Locality",
    "School District"]
FIPSToCountyDict = {"001": "Alcona County", "003": "Alger County", "005": "Allegan County", "007": "Alpena County", "009": "Antrim County", "011": "Arenac County", "013": "Baraga County", "015": "Barry County", "017": "Bay County", "019": "Benzie County", "021": "Berrien County", "023": "Branch County", "025": "Calhoun County", "027": "Cass County", "029": "Charlevoix County", "031": "Cheboygan County", "033": "Chippewa County", "035": "Clare County", "037": "Clinton County", "039": "Crawford County", "041": "Delta County", "043": "Dickinson County", "045": "Eaton County", "047": "Emmet County", "049": "Genesee County", "051": "Gladwin County", "053": "Gogebic County", "055": "Grand Traverse County", "057": "Gratiot County", "059": "Hillsdale County", "061": "Houghton County", "063": "Huron County", "065": "Ingham County", "067": "Ionia County", "069": "Iosco County", "071": "Iron County", "073": "Isabella County", "075": "Jackson County", "077": "Kalamazoo County", "079": "Kalkaska County", "081": "Kent County", "083": "Keweenaw County", "085": "Lake County", "087": "Lapeer County", "089": "Leelanau County", "091": "Lenawee County", "093": "Livingston County", "095": "Luce County", "097": "Mackinac County", "099": "Macomb County", "101": "Manistee County", "103": "Marquette County", "105": "Mason County", "107": "Mecosta County", "109": "Menominee County", "111": "Midland County", "113": "Missaukee County", "115": "Monroe County", "117": "Montcalm County", "119": "Montmorency County", "121": "Muskegon County", "123": "Newaygo County", "125": "Oakland County", "127": "Oceana County", "129": "Ogemaw County", "131": "Ontonagon County", "133": "Osceola County", "135": "Oscoda County", "137": "Otsego County", "139": "Ottawa County", "141": "Presque Isle County", "143": "Roscommon County", "145": "Saginaw County", "147": "St. Clair County", "149": "St. Joseph County", "151": "Sanilac County", "153": "Schoolcraft County", "155": "Shiawassee County", "157": "Tuscola County", "159": "Van Buren County", "161": "Washtenaw County", "163": "Wayne County", "165": "Wexford County"}
fusionData = []
millageData = []
completedData ={}

class fusionRow:
    geometry = ""
    geometry_vertex_count = 0
    school = ""
    locality = ""
    locality_name = ""
    locality_type = ""

    def __init__(self, geometry, geometry_vertex_count, locality, locality_name, locality_type, school):
        self.geometry = geometry
        self.geometry_vertex_count = geometry_vertex_count
        self.school = school
        self.locality = locality
        self.locality_name = locality_name
        self.locality_type = locality_type

    def __str__(self):
        return self.locality + "  " + self.school

class millage:
    county = ""
    locality = ""
    school = ""
    primary = 0
    secondary = 0

    def __init__(self, county, locality, school, primary, secondary):
        self.county = county
        self.locality = locality
        self.school = school
        self.primary = primary
        self.secondary = secondary

    def __str__(self):
        return self.locality + "  " + self.school + "  " + self.primary + "  " + self.secondary


with open('/Users/jim/Documents/county-locale-school-millage-2017-2018.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        data = millage(row[0], row[1], row[2], row[3], row[4])
        millageData.append(data)

# with open('/Users/jim/Downloads/schools_locales_modified.csv', 'rb') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for row in spamreader:
#         key = row[3] + row[4]
#         completedData[key] = row

def rowCompleted(row):
    ret = completedData.get(row.locality + row.school)
    return ret != None

def createFileWithHeaders():
    with open('/Users/jim/Documents/schools_locales_modified3.csv', 'w') as file:
        writer = csv.writer(file , delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(headers)

def writeFusionRow(rowData, millage):
    with open('/Users/jim/Documents/schools_locales_modified3.csv', 'a+') as file:
        writer = csv.writer(file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        row = [rowData.geometry, rowData.geometry_vertex_count, millage.county, rowData.locality,
               rowData.school, millage.primary, millage.secondary]
        writer.writerow(row)

def writeInput(row, match):
    writeFusionRow(row, match.get('millage'))

#  take county into maybe Wells Township  Escanaba Area Public Schools
def findAssociatedSchoolDistrict():
    perfectMatches = []
    nonPerfectSingleMatches = []
    manyMatches = []
    noMatches = []
    multiplePerfectMatches = []
    with open('/Users/jim/Documents/joined_school_locales.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        createFileWithHeaders()


        for row in spamreader:
            row = fusionRow(row[0], row[1], row[3], row[2], row[4], row[5])
            matches = []
            # shouldContinue = rowCompleted(row)
            # if (shouldContinue):
            #     continue

            simplifiedRowLocaleName = removeUnneededLocalityWords(row.locality.lower().strip()).strip()
            simplifiedRowSchoolName = removeUnneededSchoolWords(row.school.lower().strip()).strip()
            for millage in millageData:
                simplifiedMillageSchoolName = removeUnneededSchoolWords(millage.school.lower().strip()).strip()
                schoolMatch = schoolMatchScore(simplifiedRowSchoolName, simplifiedMillageSchoolName)

                tmpMillageLocality = millage.locality.strip()
                if (row.locality_type == "City" and "township" not in tmpMillageLocality.lower()):
                    tmpMillageLocality = "city of " + millage.locality.strip()
                simplifiedMillageLocaleName = removeUnneededLocalityWords(tmpMillageLocality.lower().strip()).strip()
                localityMatch = loalityMatchScore(simplifiedRowLocaleName, simplifiedMillageLocaleName)

                if (schoolMatch > 80 and localityMatch > 90):
                    match = {'millage': millage, 'schoolMatch': schoolMatch, 'localityMatch': localityMatch}
                    matches.append(match)

            print "\n"
            if (len(matches) == 0):
                print "no matches found for: {0}".format(row)
                noMatches.append(row)
            if (len(matches) > 1):
                print "{0} matches found for:".format(len(matches))
                matches100 = []
                for match in matches:
                    print "{0}   {1}, {2}   {3}".format(row, match.get('localityMatch'),  match.get('schoolMatch'), str(match.get('millage')))
                    if (match.get('schoolMatch') == 100 and match.get('localityMatch') == 100):
                        matches100.append(match)
                if (len(matches100) > 1):
                    multiplePerfectMatches.append(matches)
                else:
                    manyMatches.append(matches)
                bestMatch = getBestMatch(matches)
                print "choice: {0}".format(str(bestMatch.get('millage')))
                writeInput(row, bestMatch)
            if (len(matches) == 1):
                print "match found:   {0}   {1}, {2}   {3}".format(row, match.get('localityMatch'), match.get('schoolMatch'), str(match.get('millage')))
                if (matches[0].get('schoolMatch') == 100 and matches[0].get('localityMatch') == 100):
                    perfectMatches.append(matches[0])
                    writeInput(row, matches[0])
                else:
                    nonPerfectSingleMatches.append(matches[0])
                    writeInput(row, matches[0])

    print "perfect: {0}\nnps: {1}\nmany: {2}\nnoMatches: {3}\ndupPerfect: {4}"\
        .format(len(perfectMatches), len(nonPerfectSingleMatches), len(manyMatches), len(noMatches), len(multiplePerfectMatches))
    return {'perfectMatches':perfectMatches,
            'nonPerfectSingleMatches':nonPerfectSingleMatches,
            'manyMatches':manyMatches,
            'noMatches':noMatches,
            'duplicatePerfectMatches':multiplePerfectMatches}


# match found:   City of Lowell  Lowell Area Schools   79, 100     Lowell     Lowell Area School District    43.853   62.033
# Walled Lake Consolidated Schools   City of Wixom       ->       Wixom ,  Walled Lake Cons Sch Dist
# City of Orchard Lake Village   West Bloomfield School District     ->       Orchard Lake ,  West Bloomfield School Dist.
# Eagle Harbor Township    Calumet Public Schools      ->      Eagle Harbor Township ,  Public Schools Of Calumet
# Carp Lake Township   Ontonagon Area Schools     ->
# City of Galesburg   Galesburg-Augusta Community School District    ->      Galesburg   Galesburg Augusta Comm Schs
# Ingham Township   Dansville Schools     ->     Ingham Township ,  Dansville Ag School
# City of Dearborn   Dearborn City School District     ->     Dearborn ,  Dearborn City School Dist

def removeUnneededLocalityWords(str):
    tmp = str
    return tmp.replace("heights", "hts").replace("mount ", "mt ")

def removeUnneededSchoolWords(str):
    tmp = str
    return tmp.replace('schools of', '').replace('schools', '').replace('school district','').replace('school', '').replace(' schs', '') \
                .replace(' sch', '').replace('district', '').replace(' dist.', '').replace(' dist', '').replace(' sd', '').replace(' s/d', '').replace(' area', '') \
                .replace('twp', '').replace('township', '').replace('public', '').replace(' pub', '').replace(' no.', '').replace('city of ', '').replace(' city', '') \
                .replace('community', 'comm').replace('consolidated', 'cons').replace('heights', 'hgts').replace('-', ' ') \
                .replace(' agricultural', ' agr').replace(' ag ', ' agr ').replace('st.', 'st').replace("mount ", "mt ").replace("mt. ", "mt ") \
                .replace(' pointe', ' pte')


def schoolMatchScore(school1, school2):
    return fuzz.ratio(school1, school2)

def loalityMatchScore(locale1, locale2):
    return fuzz.ratio(locale1, locale2)

def getBestMatch(matches):
    bestMatch = matches[0]
    for match in matches:
        if (match.get('schoolMatch') >= bestMatch.get('schoolMatch') and
            match.get('localityMatch') >= bestMatch.get('localityMatch')):
            bestMatch = match
    return bestMatch

ret = findAssociatedSchoolDistrict()
