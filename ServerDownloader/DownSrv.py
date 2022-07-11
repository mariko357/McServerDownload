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

    stableVersion = list()
    stableVersionLink = list()
    snapshotVersion = list()
    snapshotVersionLink = list()

    async def getPageContents(url): #Non blocking function to get contents of the web page
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.read()
        return text

    def getDownloadHref(self, href): # gets file download link from web page
        try:
            page = requests.get(href)
            soupObj = BeautifulSoup(page.content, "html.parser")
            res = soupObj.find("a", string = "Download Server Jar")
            href = res.get("href")
            return href
        except:
            return None

    def getLatestDownloadHref(self): #gets latest version page
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        res = soupObj.find("span", text = "Latest Release")
        res = res.parent.parent
        soupObj = BeautifulSoup(str(res), "html.parser")
        res = soupObj.find("a", string = "Download")
        href = res.get("href")
        completeHref = self.INDEX_HREF + href
        return completeHref

    async def listStableLinkRaw(self): #gets all links to stable releases pages
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        stable = soupObj.find("h5", text = "Stable Releases")
        stableDiv = stable.parent
        elements = stableDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links

    async def listSnapshotLinkRaw(self): #Gets all links to snapshot version pages
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        snapshot = soupObj.find("h5", text = "Snapshot Preview")
        snapshotDiv = snapshot.parent
        elements = snapshotDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links

    async def listStableLink(self): #Returns links to versions that have server jar availablke to be downloaded
        rawLinks = await self.listStableLinkRaw()
        links = list()
        for i in rawLinks:
            await asyncio.sleep(0)
            if self.getDownloadHref(self.INDEX_HREF + i) != None:
                links.append(self.INDEX_HREF + i)
        return links

    async def listSnapshotLink(self): #Returns links to versions that have server jar availablke to be downloaded
        rawLinks = await self.listSnapshotLinkRaw()
        links = list()
        for i in rawLinks:
            await asyncio.sleep(0)
            if self.getDownloadHref(self.INDEX_HREF + i) != None:
                links.append(self.INDEX_HREF + i)
        return links

    async def update(self):
        self.stableVersionLink = await self.listStableLink()
        self.snapshotVersionLink = await self.listSnapshotLink()
        for i in self.stableVersionLink:
            self.stableVersion.append(self.removeToLastSlash(i))
        for i in self.snapshotVersionLink:
            self.snapshotVersion.append(self.removeToLastSlash(i))

    def removeToLastSlash(self, string):
        return re.sub(self.REGEX_REMOVE_TO_SLASH, "", string)

    def getStableLinkByVersion(self, version):
        return self.stableVersionLink[self.stableVersion.index(version)]

    def getSnapshotLinkByVersion(self, version):
        return self.snapshotVersionLink[self.snapshotVersion.index(version)]

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