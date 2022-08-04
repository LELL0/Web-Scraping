import sys
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
import json
import requests
import os
import re
import datetime
import xml.etree.ElementTree as ET
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def writeToLogs(logText):
    try:
        f = open("log.txt", "a")
        f.write("["+str(datetime.datetime.now())+"] " + str(logText)+'\n')
        f.close()
    except:
        f.close()


def getContentSelenium(url):
    try:
        from bs4 import BeautifulSoup
        from selenium import webdriver
    except:
        writeToLogs("selenium is not installed do 'pip install selenium'")
        return 0
    try:
        driver = webdriver.Chrome(executable_path='./chromedriver')
        driver.get(url)
    except:
        writeToLogs(
            "'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/home")
        return 0

    soup = BeautifulSoup(driver.page_source, features='html.parser')
    driver.quit()

    return soup


def saveFile(dict_, filename):

    json_object = json.dumps(dict_, indent=4)

    with open(filename, "w") as outfile:
        outfile.write(json_object)

    writeToLogs("Retrieved data saved at: " +
                str(os.getcwd()) + "/" + filename)


def xmlToList(fileName):
    try:
        xmlfile = ET.parse(fileName)
        xmlroot = xmlfile.getroot()
        aList = list()
        for child in xmlroot.iter():
            aList.append(child.text)
        return aList
    except:
        writeToLogs("! "+fileName +
                    " was not found, create a file and try again.")

def removeDups(dict_):
    try:
        temp = []
        result = dict()
        for key, val in dict_.items():
            if val not in temp:
                temp.append(val)
                result[key] = val
    except:
        writeToLogs("Something went wrong when removing duplicates")   
    return result


def cleanDict(socials):

    whiteList = xmlToList("socialMedia.xml")
    notAProfile = xmlToList("urlNonProfileTerms.xml")

    newDict = dict()
    for social in socials.keys():
        for key in whiteList:

            if key in social:
                while key in newDict.keys():
                    key += "_"

                try:
                    if socials[social].split("/")[3] in notAProfile:
                        pass
                    else:
                        newDict[key] = socials[social]
                        writeToLogs(socials[social])
                except:
                    pass

    return newDict


def getContentSelenium(url):
    writeToLogs("\nSCRAPING WITH Selenium ")
    writeToLogs(url)
    try:
        from bs4 import BeautifulSoup
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
    except:
        writeToLogs("selenium is not installed do 'pip install selenium'")
        return 0
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
        driver.get(url)
    except:
        writeToLogs(
            "'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/home")
        return 0

    soup = BeautifulSoup(driver.page_source, features='html.parser')
    driver.quit()

    return soup


def getcontent(url):
    writeToLogs("\nSCRAPING ")
    writeToLogs(url)
    try:
        html = requests.get(url, verify=False,
                            allow_redirects=False, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")

    except urllib.error.HTTPError as e:
        writeToLogs(
            url
            + ": '"
            + str(e.__dict__["msg"])
            + "' "
            + " Website might be protected by CAPTCHA"

        )
        return 0
    except urllib.error.URLError as e:
        writeToLogs(
            url
            + ": '"
            + str(e.__dict__["msg"])
            + "' "
            + " Website might be protected by CAPTCHA"
        )
        return 0
    except:
        return 0

    return soup


def scrape(soup):

    tags = soup("a")
    socials = dict()

    for tag in tags:
        tag = tag.get("href", None)
        try:
            key = tag.split("/")[2]
        except:
            continue

        while key in socials.keys():
            key += "_"

        socials[key.lower()] = tag.lower()

    if not socials:
        writeToLogs("! No links were Found")
        return 0

    saveFile(socials, "AllFoundUrls.json")
    socialsNoDups=removeDups(socials)
    cleanedDict = cleanDict(socialsNoDups)

    if not cleanedDict:
        writeToLogs(
            "\n! Your desired links were not found but we found other links in: "
            + str(os.getcwd())
            + "\n"
        )
        exit()

    saveFile(cleanedDict, "CleanOutput.json")


def check(url):
    try:
        r = requests.head(url)
        # urllib.request.urlopen(url)
        return r.status_code

    except urllib.error.HTTPError as e:
        writeToLogs(
            url
            + ": '"
            + str(e.__dict__["msg"])
            + "' "
            + " Website might be protected by CAPTCHA"
        )
        return e.__dict__["code"]
    except urllib.error.URLError as e:
        writeToLogs(
            url
            + ": '"
            + str(e.__dict__["msg"])
            + "' "
            + " Website might be protected by CAPTCHA"
        )
        return e.__dict__["code"]
    except:
        writeToLogs(url + ": Request ERROR")
        return 1000


def cleanurl(url):
    if "http://www." in url:
        url = url.replace("http://www.", "")
    elif "https://www." in url:
        url = url.replace("https://www.", "")
    elif "www." in url:
        url = url.replace("www.", "")
    elif "http://" in url:
        url = url.replace("http://", "")
    elif "https://" in url:
        url = url.replace("https://", "")

    writeToLogs("#" * 100)
    writeToLogs("Target to scrape: ")
    writeToLogs(url)
    writeToLogs("#" * 100 + "\n")
    return url


def checkIfIp(url):
    result = True
    match_obj = re.search(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", url)
    if match_obj is None:
        result = False
    else:
        for value in match_obj.groups():
            if int(value) > 255:
                result = False
                break
    return result


def checkInput(url):
    if checkIfIp(url):
        return "ip"
    elif (
        "http://www." in url.lower()
        or "https://www." in url.lower()
        or "www." in url.lower()
        or "http://" in url.lower()
        or "https://" in url.lower()
    ):
        return "url"
    else:
        return "domain"


def getInput():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return input("Enter url: ").strip()


url = getInput()
inputType = checkInput(url)

writeToLogs("$ input type: " + inputType)

if inputType == "ip":
    if check(url) < 400:
        if scrape(getcontent(url)) == 0:
            scrape(getContentSelenium(url))

    elif check("http://" + url) < 400:
        if scrape(getcontent("http://" + url)) == 0:
            scrape(getContentSelenium("http://" + url))
    elif check("http://" + url) < 400:
        if scrape(getcontent("https://" + url)) == 0:
            scrape(getContentSelenium("https://" + url))

elif inputType == "url":
    check(url)
    if scrape(getcontent(url)) == 0:
        scrape(getContentSelenium(url))

elif inputType == "domain":
    new_url = cleanurl(url)

    if check(new_url) < 400:
        if scrape(getcontent(new_url)) == 0:
            scrape(getContentSelenium(new_url))

    elif check("www." + new_url) < 400:
        if scrape(getcontent("www." + new_url)) == 0:
            scrape(getContentSelenium("www." + new_url))

    elif check("http://www." + new_url) < 400:
        if scrape(getcontent("http://www." + new_url)) == 0:
            scrape(getContentSelenium("http://www." + new_url))
            
    elif check("https://www." + new_url) < 400:
        if scrape(getcontent("https://www." + new_url)) == 0:
            scrape(getContentSelenium("https://www." + new_url))

    elif check("http://" + new_url) < 400:
        if scrape(getcontent("http://" + new_url)) == 0:
            scrape(getContentSelenium("http://" + new_url))

    elif check("https://" + new_url) < 400:
        if scrape(getcontent("https://" + new_url)) == 0:
            scrape(getContentSelenium("https://" + new_url))
    else:
        writeToLogs("\n! WEBSITE NOT ACCESSIBLE, COULDN'T BE SCRAPED\n")

else:
    writeToLogs("\n! WEBSITE NOT ACCESSIBLE, COULDN'T BE SCRAPED\n")
    
writeToLogs("DONE")