import os
import requests
import wget
from bs4 import BeautifulSoup

class ServerDownloader():
    VERSION = "Release 1.0"
    INDEX_HREF = "https://mcversions.net"
    BASE_HREF = "https://mcversions.net/download/"

    def getDownloadHref(self, href):
        try:
            page = requests.get(href)
            soupObj = BeautifulSoup(page.content, "html.parser")
            res = soupObj.find("a", string = "Download Server Jar")
            href = res.get("href")
            return href
        except:
            return None

    def getLatestDownloadHref(self):
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        res = soupObj.find("span", text = "Latest Release")
        res = res.parent.parent
        soupObj = BeautifulSoup(str(res), "html.parser")
        res = soupObj.find("a", string = "Download")
        href = res.get("href")
        completeHref = self.INDEX_HREF + href
        return completeHref

    def listStableLinkRaw(self):
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        stable = soupObj.find("h5", text = "Stable Releases")
        stableDiv = stable.parent
        elements = stableDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links

    def listSnapshotLinkRaw(self):
        page = requests.get(self.INDEX_HREF)
        soupObj = BeautifulSoup(page.content, "html.parser")
        snapshot = soupObj.find("h5", text = "Snapshot Preview")
        snapshotDiv = snapshot.parent
        elements = snapshotDiv.find_all("a", string = "Download")
        links = list()
        for i in elements:
            links.append(i.get("href"))
        return links

    def listStableLink(self):
        rawLinks = self.listStableLinkRaw()
        links = list()
        for i in rawLinks:
            if self.getDownloadHref(self.INDEX_HREF + i) != None:
                links.append(self.INDEX_HREF + i)
        return links

    def listSnapshotLink(self):
        rawLinks = self.listSnapshotLinkRaw()
        links = list()
        for i in rawLinks:
            if self.getDownloadHref(self.INDEX_HREF + i) != None:
                links.append(self.INDEX_HREF + i)
        return links

    def validateURL(self, href):
        try: page = requests.get(href)
        except:
            return False
        if str(page) != "<Response [404]>":
            return True
        else:
            return False

    def validatePath(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    def validateOrExit(self, validator, message):
        if not validator:
            print(message)
            exit()