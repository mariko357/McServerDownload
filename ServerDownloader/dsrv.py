import asyncio
import os
import requests
import wget
from bs4 import BeautifulSoup
import re
import aiohttp


VERSION = "Release 1.0"
INDEX_HREF = "https://mcversions.net"
BASE_DOWNLOAD_HREF = "https://mcversions.net/download/"
REGEX_REMOVE_TO_SLASH = "^(.*[\\\/])"
BAR = None
DOWNLOAD_LOCATION = ""

stableVersion = list()
stableVersionLink = list()
stableVersionDownloadLink = list()

snapshotVersion = list()
snapshotVersionLink = list()
snapshotVersionDownloadLink = list()

def init(location = "") -> None:
    update()
    global DOWNLOAD_LOCATION
    DOWNLOAD_LOCATION = location

async def getPageContents(url) -> str: #Non blocking function to get contents of the web page
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.read()
    return text

async def getDownloadHref(url) -> str: # gets file download link from link to web page (non blocking)
    try:
        page = await getPageContents(url)
        soupObj = BeautifulSoup(page, "html.parser")
        res = soupObj.find("a", string = "Download Server Jar")
        href = res.get("href")
        return href
    except:
        return None

async def getLatestDownloadHref() -> str: #gets latest version page
    page = await getPageContents(INDEX_HREF)
    soupObj = BeautifulSoup(page, "html.parser")
    res = soupObj.find("span", text = "Latest Release")
    res = res.parent.parent
    soupObj = BeautifulSoup(str(res), "html.parser")
    res = soupObj.find("a", string = "Download")
    href = res.get("href")
    completeHref = INDEX_HREF + href
    return completeHref

async def listStableLinkRaw() -> list: #gets all links to stable releases pages
    page = await getPageContents(INDEX_HREF)
    soupObj = BeautifulSoup(page, "html.parser")
    stable = soupObj.find("h5", text = "Stable Releases")
    stableDiv = stable.parent
    elements = stableDiv.find_all("a", string = "Download")
    links = list()
    for i in elements:
        links.append(i.get("href"))
    return links

async def listSnapshotLinkRaw() -> list: #Gets all links to snapshot version pages
    page = await getPageContents(INDEX_HREF)
    soupObj = BeautifulSoup(page, "html.parser")
    snapshot = soupObj.find("h5", text = "Snapshot Preview")
    snapshotDiv = snapshot.parent
    elements = snapshotDiv.find_all("a", string = "Download")
    links = list()
    for i in elements:
        links.append(i.get("href"))
    return links

async def checkDownloadable(linkToCheck, linksPointer, downLinksPointer) -> None: #checks whether page contains server jar download link
    downLink = await getDownloadHref(INDEX_HREF + linkToCheck)
    if downLink != None:
            linksPointer.append(INDEX_HREF + linkToCheck)
            downLinksPointer.append(downLink)

async def listStableLink() -> list: #Returns links to versions pages that have server jar available to be downloaded
    rawLinks = await listStableLinkRaw()
    links = list()
    downLinks = list()
    await asyncio.gather(*(checkDownloadable(i, links, downLinks) for i in rawLinks))
    return links, downLinks

async def listSnapshotLink() -> list: #Returns links to versions pages that have server jar available to be downloaded
    rawLinks = await listSnapshotLinkRaw()
    links = list()
    downLinks = list()
    await asyncio.gather(*(checkDownloadable(i, links, downLinks) for i in rawLinks))
    return links, downLinks

async def asyncUpdate() -> None: #updates version list, links to version pages, links to downloads
    global stableVersionLink, stableVersionDownloadLink, snapshotVersionLink, snapshotVersionDownloadLink
    stableVersionLink, stableVersionDownloadLink = await listStableLink()
    snapshotVersionLink, snapshotVersionDownloadLink = await listSnapshotLink()
    for i in stableVersionLink:
        stableVersion.append(removeToLastSlash(i))
    for i in snapshotVersionLink:
        snapshotVersion.append(removeToLastSlash(i))

def update() -> None:
    asyncio.run(asyncUpdate())

def removeToLastSlash(string) -> str:
    return re.sub(REGEX_REMOVE_TO_SLASH, "", string)

def getStableLinkByVersion(version) -> str: #gets link to the version page
    try:
        return stableVersionLink[stableVersion.index(version)]
    except:
        return ""
def getSnapshotLinkByVersion(version) -> str: #gets link to the version page
    try:
        return snapshotVersionLink[snapshotVersion.index(version)]
    except:
        return ""

def getLinkByVersion(version):
    if version in stableVersion:
        return getStableLinkByVersion(version)
    elif version in snapshotVersion:
        return getSnapshotLinkByVersion(version)
    else:
        return ""

def getStableDownloadLinkByVersion(version) -> str: #gets link to the downlaod link by version
    try:
        return stableVersionDownloadLink[stableVersion.index(version)]
    except:
        return ""

def getSnapshotDownloadLinkByVersion(version) -> str: #gets link to the downlaod link by version
    try:
        return snapshotVersionDownloadLink[snapshotVersion.index(version)]
    except:
        return ""

def getDownloadLinkByVersion(version):
    if version in stableVersion:
        return getStableDownloadLinkByVersion(version)
    elif version in snapshotVersion:
        return getSnapshotDownloadLinkByVersion(version)
    else:
        return ""

def downloadStableServer(version, path = "") -> None: #downloads server .jar file by version (stable)
    path = DOWNLOAD_LOCATION
    deleteIfDownloaded(version, path)
    wget.download(getStableDownloadLinkByVersion(version), f"{path}{version}.jar", bar=BAR)

def downloadSnapshotServer(version, path = "") -> None: #downloads server.jar file by version (snapshot)
    path = DOWNLOAD_LOCATION
    deleteIfDownloaded(version, path)
    wget.download(getSnapshotDownloadLinkByVersion(version), f"{path}{version}.jar", bar=BAR)

def downloadServer(version, path = ""): #downloads server only by its version (version must be in the list)
    path = DOWNLOAD_LOCATION
    if version in stableVersion:
        downloadStableServer(version, path)
    elif version in snapshotVersion:
        downloadSnapshotServer(version, path)

def isDownloaded(version, path = "") -> bool: #checks whether file is downloaded
    path = DOWNLOAD_LOCATION
    return os.path.exists(f"{path}{version}.jar")

def deleteIfDownloaded(version, path = "") -> None:
    path = DOWNLOAD_LOCATION
    if isDownloaded(version, path):
        os.remove(f"{path}{version}.jar")


def validateURL(href) -> bool: #Validates URL
    try: page = requests.get(href)
    except:
        return False
    if str(page) != "<Response [404]>":
        return True
    else:
        return False

def validatePath(path) -> bool: #Validates path
    if os.path.exists(path):
        return True
    else:
        return False

def validateOrExit(validator, message) -> None: # Passes gioven validator or exits the programm
    if not validator:
        print(message)
        exit()