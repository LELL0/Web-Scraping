from ast import Break
import sys
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
import json
import requests
import os
import re


def saveFile(dictionnaryy, filename):

    json_object = json.dumps(dictionnaryy, indent=4)

    with open(filename, "w") as outfile:
        outfile.write(json_object)

    print("Retrieved data saved at: " + os.getcwd() + "/" + filename)


def cleanDict(socials):
    newDict = dict()

    whiteList = [
        "facebook",
        "youtube",
        "instagram",
        "twitter",
        "tiktok",
        "youtube",
        "medium",
        "github",
        "linkedin",
        "reddit",
        "pinterest",
        "replit",
        "twitch",
        "drive",
    ]

    for social in socials.keys():
        for key in whiteList:
            if key in social:
                while key in newDict.keys():
                    key += "_"
                newDict[key] = socials[social]
    return newDict


def scrape(url):

    print("\nSCRAPING ", end="")
    print(url)
    html = ""
    try:
        html = requests.get(url, verify=False,allow_redirects=False)

        soup = BeautifulSoup(html.content, "html.parser")
        tags = soup("a")
        socials = dict()

        for tag in tags:
            tag = tag.get("href", None)
            print(tag)
            try:
                key = tag.split("/")[2]
            except:
                continue

            while key in socials.keys():
                key += "_"

            socials[key.lower()] = tag.lower()

        # print(socials)
        if not socials:
            print("\n! No links were Found\n")
            exit()

        saveFile(socials, "AllFoundUrls.json")
        cleanedDict = cleanDict(socials)

        if not cleanedDict:
            print(
                "\n! Your desired links were not found but we found other links in: "
                + os.getcwd()
                + "\n"
            )
            exit()

        saveFile(cleanedDict, "CleanOutput.json")

    except urllib.error.HTTPError as e:
        print(
            url
            + ": '"
            + e.__dict__["msg"]
            + "' "
            + " Website might be protected by CAPTCHA"
        )
    except urllib.error.URLError as e:
        print(
            url
            + ": '"
            + e.__dict__["msg"]
            + "' "
            + " Website might be protected by CAPTCHA"
        )


def check(url):
    try:
        r = requests.head(url)
        urllib.request.urlopen(url)
        return r.status_code

    except urllib.error.HTTPError as e:
        print(
            url
            + ": '"
            + e.__dict__["msg"]
            + "' "
            + " Website might be protected by CAPTCHA"
        )
        return e.__dict__["code"]
    except urllib.error.URLError as e:
        print(
            url
            + ": '"
            + e.__dict__["msg"]
            + "' "
            + " Website might be protected by CAPTCHA"
        )
        return e.__dict__["code"]
    except:
        print(url + ": Request ERROR")
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

    print("\n" + "#" * 100)
    print("Target to scrape: ", end="")
    print(url)
    print("#" * 100 + "\n")
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

print("$ input type: " + inputType)

if inputType == "ip":
    if check(url) < 400:
        scrape(url)

    elif check("http://" + url) < 400:
        scrape("http://" + url)

    elif check("http://" + url) < 400:
        scrape("https://" + url)

elif inputType == "url":
    check(url)
    scrape(url)

elif inputType == "domain":
    new_url = cleanurl(url)

    if check(new_url) < 400:
        scrape(new_url)

    elif check("www." + new_url) < 400:
        scrape("www." + new_url)

    elif check("http://www." + new_url) < 400:
        scrape("http://www." + new_url)

    elif check("https://www." + new_url) < 400:
        scrape("https://www." + new_url)

    elif check("http://" + new_url) < 400:
        scrape("http://" + new_url)

    elif check("https://" + new_url) < 400:
        scrape("https://" + new_url)

    else:
        print("\n! WEBSITE NOT ACCESSIBLE, COULDN'T BE SCRAPED\n")

else:
    print("\n! WEBSITE NOT ACCESSIBLE, COULDN'T BE SCRAPED\n")
