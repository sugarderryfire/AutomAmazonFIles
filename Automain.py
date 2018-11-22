import stem.process
from stem import Signal
from stem.control import Controller
from splinter import Browser
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl
import urllib2
import random
import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os



proxyIP = "127.0.0.1"
proxyPort = 9150
lastIP = "0.0.0.0"
currentIP = "0.0.0.0"
urlIP = "http://www.icanhazip.com"
googleURL = "http://www.google.co.il"
fileName = r'c:\temp\File.xlsx'
travels = ['t1', 't2', 't3', 't4', 't5', 't6']  # columns name of the pages that need to be travel.
geoLocationURL=r'http://www.geoplugin.net/json.gp?ip='
playStoreURL=r'https://play.google.com/store'
fileNameWords=r'words.xlsx'
searchIDbutton='gbqfq'
playStoreSearch=r'https://play.google.com/store/search?q='



def AutomateBrowse():
    """df = pd.read_excel(fileName, sheet_name='Sheet1')  # open the db
    # get the keyword and the url from db:
    keywordsList = df['keyword']
    sitesList = df['site']
    t1 = df[travels[0]]  # get page position 0 that need to be traveled for all the sites.
    t2 = df[travels[1]]
    t3 = df[travels[2]]
    t4 = df[travels[3]]
    t5 = df[travels[4]]
    t6 = df[travels[5]]"""
    proxy_settings = {"network.proxy.type":1,
        "network.proxy.socks": proxyIP,
        "network.proxy.socks_port": proxyPort,
        "network.proxy.socks_remote_dns": True
    }
    cap = DesiredCapabilities().FIREFOX.copy()
    cap["marionette"] = False
    browser = Browser('firefox',capabilities={'acceptSslCerts': True})
    checkIP(browser)  # get the first IP
    #browser.visit(url2)  # visit google
    print currentIP
    time.sleep(6)
    #AlternateID(browser)
    print currentIP

def readWordsExcel():
    df = pd.read_excel(fileNameWords, sheet_name='Sheet1')  # open the db
    IDlist=df['ID']
    keywordsList = df['keyword']
    return keywordsList,IDlist


def start_requests():
    #keywordsList, IDlist = readWordsExcel()
    key=sys.argv[1]
    currentID=sys.argv[2]
    cap = DesiredCapabilities().FIREFOX.copy()
    cap["marionette"] = False
    browser = Browser('firefox',capabilities={'acceptSslCerts': True})
    browse(browser, key, currentID)
    browser.quit()
    file = open("finish.txt", "wb")
    file.close()




def browse(browser, key,currentID):
    browser.visit(playStoreURL)
    time.sleep(8)
    playStoreSearchFill=playStoreSearch+key
    browser.visit(playStoreSearchFill)
    #search = browser.find_by_id(searchIDbutton)
    #search.type('type',key)
    #search.fill('\n')
    #search.send_keys(Keys.RETURN)
    time.sleep(10)
    loadMoreResults(browser, 3)
    appText='Blockchain Technology Course'
    childTag=browser.find_link_by_partial_href(currentID)
    parentTag=childTag.find_by_xpath('..').click()
    time.sleep(5)
    jumpDown(browser)
    time.sleep(generateRandomINT(210, 360))
    jumpUp(browser)
    time.sleep(30)


def clickParent(childTag):
    try:
        parentTag=childTag.find_element_by_xpath('..')
        parentTag.click()
    except:
        try:
            parentTag=childTag.find_element_by_xpath('..')
            parentTag.click()
        except:
            print "cant click on the link. exit"



def jumpDown(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def jumpUp(browser):
    browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")


def loadMoreResults(browser,pages):
    for i in range(1,pages):
        jumpDown(browser)
        time.sleep(3)


def generateRandomINT(min1,max1):
    generatedNum=random.randint(min1-1,max1-1)
    return generatedNum


def AlternateID(browser):
    global currentIP, lastIP
    while(True):
        lastIP=currentIP
        switchIP()
        checkIP(browser)  # get current IP
        #time.sleep(5)
        if lastIP != currentIP and checkUSA(currentIP):
            break


def checkIP(browser):
    global currentIP, urlIP, lastIP
    browser.visit(urlIP)  # visit url to get the current IP
    time.sleep(3)
    if urlIP in browser.url:
        lastIP = currentIP
        currentIP = browser.find_by_tag('pre').first.value


def checkUSA(tempIP):
    fullURL=geoLocationURL+tempIP
    response = urllib2.urlopen(fullURL)
    html = response.read()
    if "United States" in html:
        print "United States"
        return True
    else:
        print 'other'
        return False


def switchIP():
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def main():
    start_requests()
    #sys.exit(0)



if __name__=="__main__":
    main()



