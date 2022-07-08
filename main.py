import wget
import requests
from bs4 import BeautifulSoup

URL = "https://mcversions.net/download/1.18.2"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
res = soup.find("a", string = "Download Server Jar")
href = res.get("href")
print(href)