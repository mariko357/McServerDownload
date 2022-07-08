import wget
import requests
from bs4 import BeautifulSoup
import argparse

VERSION = "1.0"
BASE_HREF = "https://mcversions.net/download/"
def getDownloadHref(href):
    page = requests.get(href)
    soupObj = BeautifulSoup(page.content, "html.parser")
    res = soupObj.find("a", string = "Download Server Jar")
    href = res.get("href")
    return href

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Server Jar File")

    parser.add_argument("--verison", "-v", action="version", version=VERSION, help="Programm Verison")
    parser.add_argument("--download", "-d", help="Download Specific Server Version", type = str)
    parser.add_argument("--link", "-l", help="Download Server From Specific Link", type = str)
    parser.add_argument("--path", "-p", help="Select download path", type = str)
    parser.add_argument("--bar", "-b", help="Display download bar (true/false), Default = false", nargs = "?", const = "false", type = str)

    options, args = parser.parse_known_args()


    if options.link:
        if options.path:
            wget.download(options.link, options.path)
        else:
            wget.download(options.link)

    elif options.download:

        href = BASE_HREF + options.download
        downHref = getDownloadHref(href)

        if options.path:
            wget.download(downHref, options.path)
        else:
            wget.download(downHref)
        
    else:
        print("No arguments provided! Exiting without action!")
    