import wget
import requests
from bs4 import BeautifulSoup
import argparse
import os
import ServerDownloader

VERSION = "Release 1.0"
INDEX_HREF = "https://mcversions.net"
BASE_HREF = "https://mcversions.net/download/"

def getDownloadHref(href):
    try:
        page = requests.get(href)
        soupObj = BeautifulSoup(page.content, "html.parser")
        res = soupObj.find("a", string = "Download Server Jar")
        href = res.get("href")
        return href
    except:
        return None

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

def listStableLinkRaw():
    page = requests.get(INDEX_HREF)
    soupObj = BeautifulSoup(page.content, "html.parser")
    stable = soupObj.find("h5", text = "Stable Releases")
    stableDiv = stable.parent
    elements = stableDiv.find_all("a", string = "Download")
    links = list()
    for i in elements:
        links.append(i.get("href"))
    return links

def listSnapshotLinkRaw():
    page = requests.get(INDEX_HREF)
    soupObj = BeautifulSoup(page.content, "html.parser")
    snapshot = soupObj.find("h5", text = "Snapshot Preview")
    snapshotDiv = snapshot.parent
    elements = snapshotDiv.find_all("a", string = "Download")
    links = list()
    for i in elements:
        links.append(i.get("href"))
    return links

def listStableLink():
    rawLinks = listStableLinkRaw()
    links = list()
    for i in rawLinks:
        if getDownloadHref(INDEX_HREF + i) != None:
            links.append(INDEX_HREF + i)
    return links

def listSnapshotLink():
    rawLinks = listSnapshotLinkRaw()
    links = list()
    for i in rawLinks:
        if getDownloadHref(INDEX_HREF + i) != None:
            links.append(INDEX_HREF + i)
    return links

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
    inst = ServerDownloader()
    
    """parser = argparse.ArgumentParser(description="Download Server Jar File")

    parser.add_argument("--verison", "-v", action="version", version=VERSION, help="Programm Verison")
    parser.add_argument("--download", "-d", help="Download Specific Server Version", type = str)
    parser.add_argument("--url", "-u", help="Download Server From Specific URL", type = str)
    parser.add_argument("--path", "-p", help="Select download path", type = str)
    parser.add_argument("--latest", "-l", help="Download Latest Release Version", nargs = "?", const = "true", default = "false", type = str)
    parser.add_argument("--bar", "-b", help="Display download bar", nargs = "?", const = "true", default = "false", type = str)
    parser.add_argument("--stable", help="Lists all", type = str)
    parser.add_argument("--snapshot", help="Select download path", type = str)

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
        print("No arguments provided! Exiting without action")"""
    links = listStableLink()
    total = len(links)
    j = 0
    for i in links:
        j += 1
        print(f"{j} Out Of {total}; ", end=" ")
        print(i.removeprefix("https://mcversions.net/download/"), end = ": ")
        print(i)