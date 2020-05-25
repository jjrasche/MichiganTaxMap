from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

PAGE_LOAD_WAIT = 55
driver = webdriver.PhantomJS()
driver.set_page_load_timeout(PAGE_LOAD_WAIT)
alreadyFound = "alreadyFound"
noRecord = "noRecord"
badAddress = "badAddress"
timeOutException = "timeout"

def saveScreenShot():
    driver.save_screenshot('screenshot.png')

def noParcelFound(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup.find("div", "sresult-detail-norecord-found") != None

def goto(url):
    driver.get(url)
    # print("navigating to: {0}".format(url))
    return getPageSource()

def getPageSource():
    return BeautifulSoup(driver.page_source, "html.parser")

def browseUrlByClass(url, waitClass):
    goto(url)
    if waitClass != None:
        try:
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.CLASS_NAME, waitClass)))
        except Exception:
            if noParcelFound(driver):
                return noRecord
            raise Exception
        finally:
            saveScreenShot()
    return getPageSource()

def browseUrlById(url, waitClass):

    goto(url)
    if waitClass != None:
        try:
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.ID, waitClass)))
        except Exception:
            if noParcelFound(driver):
                return noRecord
            raise Exception
        finally:
            saveScreenShot()
    return getPageSource()

def browseUrl(url, text):
    goto(url)
    if text != None:
        try:
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, text)))
        except Exception:
            raise Exception
        finally:
            saveScreenShot()
    return getPageSource()

def browseOnAction(action, element):
    try:
        action()
        loadType = list(element)[0]
        loadIdentifier = element[loadType]
        if (loadType == "class"):
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.CLASS_NAME, loadIdentifier)))
        elif (loadType == "text"):
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, loadIdentifier)))
            saveScreenShot()
    except NoSuchElementException:
        print("no element found with text {0}".format(element))
    except TimeoutException:
        print("timeout on element: {0}\n error:{1}".format(element, TimeoutException))
        return timeOutException
    except Exception:
        raise Exception
    finally:
        saveScreenShot()
        # print("BOA navigating to: {0}".format(driver.current_url))
    return BeautifulSoup(driver.page_source, "html.parser")


def findElementsInListByText(list, text):
    elements = []
    for ele in list:
        if ele.text.find(text) != -1:
            elements.append(ele)
    return elements[0] if len(elements) > 0 else None