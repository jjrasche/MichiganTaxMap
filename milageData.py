from browsingFunctionaliy import alreadyFound, noRecord, browseUrlByClass, browseOnAction, findElementsInListByText, driver, goto
import datetime
from datetime import timedelta
import time

def wait(seconds):
    startTime = datetime.datetime.now()
    while (datetime.datetime.now() < startTime + timedelta(seconds=seconds)):
        time.sleep(1)

countyId = "County"
localId = "LocalUnit"
schoolId = "SchoolDistrict"
url = "https://treas-secure.state.mi.us/ptestimator/PTEstimator.asp"
data = ""
blah = ""

def getOptionElement(id, index):
    return driver.find_element_by_id(id).find_elements_by_tag_name("option")[index]

def getNumberOfOptions(id):
    return len(driver.find_element_by_id(id).find_elements_by_tag_name("option"))

def clickOption(element):
    browseOnAction(lambda: element.click(), {"class": "header"})

def getPagedData(url):
    browseUrlByClass(url, "header")
    ret = ""
    try:
        numCountyOptions = getNumberOfOptions(countyId)
        for countyOptionIndex in range(82, numCountyOptions):
            countyOption = getOptionElement(countyId, countyOptionIndex)
            countyName = countyOption.text.strip()
            clickOption(countyOption)

            numLocalOptions = getNumberOfOptions(localId)
            localStart = 1
            # if (countyName == "Huron County"):
            #     localStart = 5

            for localOptionIndex in range(localStart, numLocalOptions):
                localOption = getOptionElement(localId, localOptionIndex)
                localName = localOption.text
                clickOption(localOption)

                wait(2)

                for school in driver.find_element_by_id(schoolId).find_elements_by_tag_name("option"):
                    if (school.text == "Select One"):
                        continue
                    rates = school.get_attribute('value')

                    homeSteadRate, nonHomeSteadRate = rates.split(";")
                    str = "{0}, {1}, {2}, {3}, {4}".format(countyName, localName, school.text, homeSteadRate, nonHomeSteadRate)
                    ret += str + "\n"
    except Exception, e:
        pause = 5
        print ret
        raise
    return ret

d = getPagedData(url)

after = 5