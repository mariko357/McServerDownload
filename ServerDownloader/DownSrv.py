import os
import requests
import wget
from bs4 import BeautifulSoup
import re

class ServerDownloader():
    VERSION = "Release 1.0"
    INDEX_HREF = "https://mcversions.net"
    BASE_HREF = "https://mcversions.net/download/"
    REGEX_REMOVE_TO_SLASH = "^(.*[\\\/])"

    stableVersion = list()
    stableVersionLink = list()
    snapshotVersion = list()
    snapshotVersionLink = list()

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

    def listStableLinkRaw(self): #gets all links to stable releases pages
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        stable = soupObj.find("h5", text = "Stable Releases")
        stableDiv = stable.parent
        elements = stableDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links

    def listSnapshotLinkRaw(self): #Gets all links to snapshot version pages
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        snapshot = soupObj.find("h5", text = "Snapshot Preview")
        snapshotDiv = snapshot.parent
        elements = snapshotDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links

    def listStableLink(self): #Returns links to versions that have server jar availablke to be downloaded
        rawLinks = self.listStableLinkRaw()
        links = list()
        for i in rawLinks:
            if self.getDownloadHref(self.INDEX_HREF + i) != None:
                links.append(self.INDEX_HREF + i)
        return links

    def listSnapshotLink(self): #Returns links to versions that have server jar availablke to be downloaded
        rawLinks = self.listSnapshotLinkRaw()
        links = list()
        for i in rawLinks:
            if self.getDownloadHref(self.INDEX_HREF + i) != None:
                links.append(self.INDEX_HREF + i)
        return links

    def update(self):
        self.stableVersionLink = self.listStableLink()
        self.snapshotVersionLink = self.listSnapshotLink()
        for i in self.stableVersionLink:
            self.stableVersion.append(self.removeToLastSlash(i))
        for i in self.snapshotVersionLink:
            self.snapshotVersion.append(self.removeToLastSlash(i))

    def removeToLastSlash(self, string):
        return re.sub(self.REGEX_REMOVE_TO_SLASH, "", string)

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