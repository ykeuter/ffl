import requests
from bs4 import BeautifulSoup

url = "http://games.espn.com/ffl/tools/projections"

page = requests.get(url)

soup = BeautifulSoup(page.content, "lxml")

p = soup.select("tr.pncPlayerRow td.playertablePlayerName")[0]
