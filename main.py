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

def validateURL(href):
    page = requests.get(href)
    if str(page) != "<Response [404]>":
        return True
    else:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Server Jar File")

    parser.add_argument("--verison", "-v", action="version", version=VERSION, help="Programm Verison")
    parser.add_argument("--download", "-d", help="Download Specific Server Version", type = str)
    parser.add_argument("--link", "-l", help="Download Server From Specific Link", type = str)
    parser.add_argument("--path", "-p", help="Select download path", type = str)
    parser.add_argument("--bar", "-b", help="Display download bar", nargs = "?", const = "true", default = "false", type = str)

    options, args = parser.parse_known_args()

    if options.bar != "false":
        bar = wget.bar_adaptive
    else:
        bar = None


    if options.link:
        if options.path:
            wget.download(options.link, options.path, bar = bar)
        else:
            wget.download(options.link, bar = bar)

    elif options.download:

        href = BASE_HREF + options.download

        if validateURL(href):

            downHref = getDownloadHref(href)

            if options.path:
                wget.download(downHref, options.path, bar = bar)
            else:
                wget.download(downHref, bar = bar)
        else:
            print("No such verison")
            exit()
        
    else:
        print("No arguments provided! Exiting without action!")
    