import asyncio
import os
import requests
import wget
from bs4 import BeautifulSoup
import re
import asyncio
import aiohttp

class ServerDownloader():
    VERSION = "Release 1.0"
    INDEX_HREF = "https://mcversions.net"
    BASE_HREF = "https://mcversions.net/download/"
    REGEX_REMOVE_TO_SLASH = "^(.*[\\\/])"
    BAR = None
    DOWNLOAD_LOCATION = ""

    stableVersion = list()
    stableVersionLink = list()
    stableVersionDownloadLink = list()

    snapshotVersion = list()
    snapshotVersionLink = list()
    snapshotVersionDownloadLink = list()

    async def getPageContents(self, url): #Non blocking function to get contents of the web page
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.read()
        return text

    async def getDownloadHref(self, url): # gets file download link from link to web page (non blocking)
        try:
            page = await self.getPageContents(url)
            soupObj = BeautifulSoup(page, "html.parser")
            res = soupObj.find("a", string = "Download Server Jar")
            href = res.get("href")
            return href
        except:
            return None

    async def getLatestDownloadHref(self): #gets latest version page
        page = await self.getPageContents(self.INDEX_HREF)
        soupObj = BeautifulSoup(page, "html.parser")
        res = soupObj.find("span", text = "Latest Release")
        res = res.parent.parent
        soupObj = BeautifulSoup(str(res), "html.parser")
        res = soupObj.find("a", string = "Download")
        href = res.get("href")
        completeHref = self.INDEX_HREF + href
        return completeHref

    async def listStableLinkRaw(self): #gets all links to stable releases pages
        page = await self.getPageContents(self.INDEX_HREF)
        soupObj = BeautifulSoup(page, "html.parser")
        stable = soupObj.find("h5", text = "Stable Releases")
        stableDiv = stable.parent
        elements = stableDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links

    async def listSnapshotLinkRaw(self): #Gets all links to snapshot version pages
        page = await self.getPageContents(self.INDEX_HREF)
        soupObj = BeautifulSoup(page, "html.parser")
        snapshot = soupObj.find("h5", text = "Snapshot Preview")
        snapshotDiv = snapshot.parent
        elements = snapshotDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links
    
    async def checkDownloadable(self, linkToCheck, linksPointer, downLinksPointer):
        downLink = await self.getDownloadHref(self.INDEX_HREF + linkToCheck)
        if downLink != None:
                linksPointer.append(self.INDEX_HREF + linkToCheck)
                downLinksPointer.append(downLink)

    async def listStableLink(self): #Returns links to versions pages that have server jar available to be downloaded
        rawLinks = await self.listStableLinkRaw()
        links = list()
        downLinks = list()
        await asyncio.gather(*(self.checkDownloadable(i, links, downLinks) for i in rawLinks))
        return links, downLinks

    async def listSnapshotLink(self): #Returns links to versions pages that have server jar available to be downloaded
        rawLinks = await self.listSnapshotLinkRaw()
        links = list()
        downLinks = list()
        await asyncio.gather(*(self.checkDownloadable(i, links, downLinks) for i in rawLinks))
        return links, downLinks

    async def asyncUpdate(self): #updates version list, links to version pages, links to downloads
        self.stableVersionLink, self.stableVersionDownloadLink = await self.listStableLink()
        self.snapshotVersionLink, self.snapshotVersionDownloadLink = await self.listSnapshotLink()
        for i in self.stableVersionLink:
            self.stableVersion.append(self.removeToLastSlash(i))
        for i in self.snapshotVersionLink:
            self.snapshotVersion.append(self.removeToLastSlash(i))
    
    def update(self):
        asyncio.run(self.asyncUpdate())

    def removeToLastSlash(self, string):
        return re.sub(self.REGEX_REMOVE_TO_SLASH, "", string)

    def getStableLinkByVersion(self, version): #gets link to the version page
        return self.stableVersionLink[self.stableVersion.index(version)]

    def getSnapshotLinkByVersion(self, version): #gets link to the version page
        return self.snapshotVersionLink[self.snapshotVersion.index(version)]

    def getStableLinkByVersion(self, version): #gets link to the downlaod link by version
        return self.stableVersionDownloadLink[self.stableVersion.index(version)]

    def getSnapshotLinkByVersion(self, version): #gets link to the downlaod link by version
        return self.snapshotVersionDownloadLink[self.snapshotVersion.index(version)]

    def validateURL(self, href): #Validates URL
        try: page = requests.get(href)
        except:
            return False
        if str(page) != "<Response [404]>":
            return True
        else:
            return False

    def validatePath(self, path): #Validates path
        if os.path.exists(path):
            return True
        else:
            return False

    def validateOrExit(self, validator, message): # Passes gioven validator or exits the programm
        if not validator:
            print(message)
            exit()