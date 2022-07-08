import wget
import requests
from bs4 import BeautifulSoup
import argparse
import os
import re

VERSION = "Release 1.0"
INDEX_HREF = "https://mcversions.net"
BASE_HREF = "https://mcversions.net/download/"

def getDownloadHref(href):
    page = requests.get(href)
    soupObj = BeautifulSoup(page.content, "html.parser")
    res = soupObj.find("a", string = "Download Server Jar")
    href = res.get("href")
    return href

def getLatestDownloadHref():
    page = requests.get(INDEX_HREF)
    soupObj = BeautifulSoup(page.content, "html.parser")
    res = soupObj.find("span", text = "Latest Release")
    res = res.parent.parent
    soupObj = BeautifulSoup(str(res), "html.parser")
    res = soupObj.find("a", string = "Download")
    href = res.get("href")
    completeHref = INDEX_HREF + href
    return completeHref


def validateURL(href):
    try: page = requests.get(href)
    except:
        return False
    if str(page) != "<Response [404]>":
        return True
    else:
        return False

def validatePath(path):
    if os.path.exists(path):
        return True
    else:
        return False

def validateOrExit(validator, message):
    if not validator:
        print(message)
        exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Server Jar File")

    parser.add_argument("--verison", "-v", action="version", version=VERSION, help="Programm Verison")
    parser.add_argument("--download", "-d", help="Download Specific Server Version", type = str)
    parser.add_argument("--url", "-u", help="Download Server From Specific URL", type = str)
    parser.add_argument("--path", "-p", help="Select download path", type = str)
    parser.add_argument("--latest", "-l", help="Download Latest Release Version", nargs = "?", const = "true", default = "false", type = str)
    parser.add_argument("--bar", "-b", help="Display download bar", nargs = "?", const = "true", default = "false", type = str)

    options, args = parser.parse_known_args()

    if options.bar != "false":
        bar = wget.bar_adaptive
    else:
        bar = None

    if options.latest != "false":
        href = getLatestDownloadHref()
        validateOrExit(validateURL(href), "No such version")
        downHref = getDownloadHref(href)

        if options.path:
            validateOrExit(validatePath(options.path), "No such path")
            wget.download(downHref, options.path, bar = bar)
        else:
            wget.download(downHref, bar = bar)

    elif options.url:
        validateOrExit(validateURL(options.url), "Link is invalid")
        if options.path:
            validateOrExit(validatePath(options.path), "No such path")
            wget.download(options.url, options.path, bar = bar)
        else:
            wget.download(options.url, bar = bar)

    elif options.download:
        href = BASE_HREF + options.download
        validateOrExit(validateURL(href), "No such version")
        downHref = getDownloadHref(href)

        if options.path:
            validateOrExit(validatePath(options.path), "No such path")
            wget.download(downHref, options.path, bar = bar)
        else:
            wget.download(downHref, bar = bar)
        
    else:
        print("No arguments provided! Exiting without action!")
    