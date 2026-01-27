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


def displayResultFromJson(fileName):
    try:
        f = open(fileName+".json")
        print(f.read())
    except:
        pass


def saveFile(dictionary, fileName):
    try:
        with open(fileName+".json", "w") as outfile:
            json.dump(dictionary, outfile)
    except:
        pass


def xmlToList(fileName):
    try:
        xmlfile = ET.parse(fileName)
        xmlroot = xmlfile.getroot()
        aList = list()
        for child in xmlroot.iter():
            if child.text.strip():
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

    newDictKeys = list(newDict.keys())
    for key in whiteList:
        if not key in newDictKeys:
            newDict[key] = "N/A"
    return newDict


def getContentSelenium(url):
    writeToLogs("\nSCRAPING WITH Selenium ")
    writeToLogs(url)
    try:
        from bs4 import BeautifulSoup
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
    except:
        writeToLogs("selenium is not installed do 'pip install selenium'")
        return 0
    try:
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(
            executable_path='./geckodriver', options=options)
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


MIN_PHONE_DIGITS = 9
PHONE_ALLOWED_CHARS = set('0123456789 -\\')


def normalize_phone(raw):
    """Keep only digits, space, backslash and hyphen. Collapse spaces."""
    if not raw:
        return ''
    s = ''.join(c for c in raw if c in PHONE_ALLOWED_CHARS)
    return re.sub(r'\s+', ' ', s).strip()


def is_valid_phone(digits):
    """Return True only if digits look like a real phone number (9+ digits)."""
    if not digits or not digits.isdigit():
        return False
    n = len(digits)
    if n < MIN_PHONE_DIGITS or n > 15:
        return False
    if len(set(digits)) == 1:
        return False
    if len(set(digits)) < 3:
        return False
    if n == 4 and digits.startswith(('19', '20')):
        return False
    if n == 8 and digits.startswith(('19', '20')):
        return False
    if n == 8 and digits[:4].isdigit() and digits[4:6].isdigit() and digits[6:8].isdigit():
        y, m, d = int(digits[:4]), int(digits[4:6]), int(digits[6:8])
        if 1990 <= y <= 2030 and 1 <= m <= 12 and 1 <= d <= 31:
            return False
    if n >= MIN_PHONE_DIGITS and digits == ''.join(sorted(digits)):
        return False
    if n >= MIN_PHONE_DIGITS and digits == ''.join(sorted(digits, reverse=True)):
        return False
    return True


def extract_emails_and_phones(soup):
    """Extract emails and phone numbers. Phones: 9+ digits, only digits/space/\\/-."""
    emails = set()
    phones = set()
    email_pattern = re.compile(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    )
    phone_pattern = re.compile(
        r'(?:[0-9][\s\-\\]*){9,}'
    )

    def add_emails_from_text(s):
        if not s:
            return
        for m in email_pattern.finditer(s):
            emails.add(m.group())

    def add_phones_from_text(s, require_separator=True):
        if not s:
            return
        for m in phone_pattern.finditer(s):
            raw = m.group().strip()
            normalized = normalize_phone(raw)
            digits = re.sub(r'[\s\-\\]', '', normalized)
            if len(digits) < MIN_PHONE_DIGITS or len(digits) > 15 or len(normalized) > 30:
                continue
            if not is_valid_phone(digits):
                continue
            # When scanning body, require at least one space \- or \ (avoids long digit dumps)
            if require_separator and ' ' not in normalized and '-' not in normalized and '\\' not in normalized:
                continue
            phones.add(normalized)

    try:
        # 1) mailto: and tel: links (most reliable)
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('mailto:'):
                addr = href[7:].split('?')[0].strip()
                if '@' in addr and '.' in addr:
                    emails.add(addr)
            elif href.startswith('tel:'):
                raw = href[4:].strip()
                digits = re.sub(r'\D', '', raw)
                if len(digits) >= MIN_PHONE_DIGITS and is_valid_phone(digits):
                    # Store normalized (digits only or digits + space \- \\)
                    phones.add(normalize_phone(raw) or digits)
                    link_text = (a.get_text() or '').strip()
                    if link_text:
                        lt_digits = re.sub(r'\D', '', link_text)
                        if lt_digits == digits:
                            phones.add(normalize_phone(link_text) or digits)

        # 2) meta description / og:description – short, curated; allow digits-only if 9+
        for meta in soup.find_all('meta', attrs={'content': True}):
            content = meta.get('content') or ''
            if not content:
                continue
            name = (meta.get('name') or meta.get('property') or '').lower()
            if 'description' in name or 'og:description' in name:
                add_emails_from_text(content)
                add_phones_from_text(content, require_separator=False)

        # 3) Visible text – require space \- or \ (avoids IDs/versions in scripts)
        text = soup.get_text(separator=' ')
        add_emails_from_text(text)
        add_phones_from_text(text, require_separator=True)

        # 4) Raw HTML for emails only (phones from raw HTML are too noisy: versions, script data)
        raw_html = str(soup)
        add_emails_from_text(raw_html)
    except Exception as e:
        writeToLogs("Error extracting emails/phones: " + str(e))

    # Remove duplicates: emails by lowercase, phones by digit sequence
    seen_email = {}
    for e in emails:
        k = e.lower()
        if k not in seen_email:
            seen_email[k] = e
    emails_deduped = list(seen_email.values())

    # Phones: dedupe by digit sequence, then store as digits only (no spaces or special chars)
    seen_phone_digits = {}
    for p in phones:
        digits = re.sub(r'[\s\-\\]', '', p)
        if digits not in seen_phone_digits:
            seen_phone_digits[digits] = digits
    phones_deduped = list(seen_phone_digits.values())

    return emails_deduped, phones_deduped


def scrape(soup):
    try:
        tags = soup("a")
        socials = dict()
    except:
        writeToLogs("ERROR while getting tags from soup")

    try:
        for tag in tags:
            tag = tag.get("href", None)
            try:
                key = tag.split("/")[2]
            except:
                continue

            while key in socials.keys():
                key += "_"

            socials[key.lower()] = tag.lower()
    except:
        writeToLogs("error splitting tags")

    # Extract emails and phone numbers from page
    emails, phones = extract_emails_and_phones(soup)

    saveFile(socials, "AllFoundUrls")
    socialsNoDups = removeDups(socials)
    cleanedDict = cleanDict(socialsNoDups)

    # Add emails and phones to output
    cleanedDict["emails"] = emails
    cleanedDict["phones"] = phones

    if not cleanedDict and not emails and not phones:
        writeToLogs(
            "\n! Your desired links were not found but we found other links in: "
            + str(os.getcwd())
            + "\n"
        )
        return None

    emptyDict = True
    for elm in cleanedDict:
        if elm not in ("emails", "phones") and cleanedDict[elm] != "N/A":
            emptyDict = False

    return cleanedDict


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
    try:
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
    except:
        writeToLogs("ERROR cleaning the URL")
    return url


def checkIfIp(url):
    try:
        result = True
        match_obj = re.search(
            r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", url)
        if match_obj is None:
            result = False
        else:
            for value in match_obj.groups():
                if int(value) > 255:
                    result = False
                    break
    except:
        writeToLogs("ERROR checking if its an IP")
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
    """Return list of URLs from terminal input. User enters URL(s) separated by commas."""
    prompt = "Enter URL(s) separated by commas: "
    while True:
        raw = input(prompt).strip()
        if not raw:
            prompt = "No input. Enter URL(s) separated by commas: "
            continue
        urls = [u.strip() for u in raw.split(",") if u.strip()]
        if urls:
            return urls
        prompt = "No valid URLs. Enter URL(s) separated by commas: "


def process_url(url):
    """Fetch and scrape one URL; return result dict or None."""
    inputType = checkInput(url)
    writeToLogs("$ input type: " + inputType + " for " + url)

    def try_scrape(fetch_url):
        content = getcontent(fetch_url)
        if content:
            result = scrape(content)
            if result is not None:
                return result
        content = getContentSelenium(fetch_url)
        if content:
            return scrape(content)
        return None

    if inputType == "ip":
        if check(url) < 400:
            return try_scrape(url)
        if check("http://" + url) < 400:
            return try_scrape("http://" + url)
        if check("https://" + url) < 400:
            return try_scrape("https://" + url)

    elif inputType == "url":
        check(url)
        return try_scrape(url)

    elif inputType == "domain":
        new_url = cleanurl(url)
        for try_url in [new_url, "www." + new_url, "http://www." + new_url,
                        "https://www." + new_url, "http://" + new_url, "https://" + new_url]:
            if check(try_url) < 400:
                result = try_scrape(try_url)
                if result is not None:
                    return result
        writeToLogs("\n! WEBSITE NOT ACCESSIBLE: " + url + "\n")
        return None

    else:
        writeToLogs("\n! WEBSITE NOT ACCESSIBLE: " + url + "\n")
        return None


urls = getInput()
if not urls:
    writeToLogs("! No URLs provided.")
    sys.exit(1)

all_results = {}
for url in urls:
    result = process_url(url)
    if result is not None:
        key = url if ("://" in url or url.startswith("www.")) else url
        all_results[key] = result

if all_results:
    if len(all_results) == 1:
        saveFile(next(iter(all_results.values())), "CleanOutput")
    else:
        saveFile(all_results, "CleanOutput")
else:
    saveFile({}, "CleanOutput")

displayResultFromJson("CleanOutput")

writeToLogs("DONE")
