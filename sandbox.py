import requests
from bs4 import BeautifulSoup

api_url = \
    "https://registerdisney.go.com/jgc/v5/client/ESPN-ESPNCOM-PROD/api-key?langPref=en-US"
login_url = \
    "https://ha.registerdisney.go.com/jgc/v5/client/ESPN-ESPNCOM-PROD/guest/login?langPref=en-US"

login_json = '{"loginValue": "ykeuter@me.com", "password": "TP!@8nRZBD2a"}'

s = requests.Session()

# soup = BeautifulSoup(page.content, "lxml")

# p = soup.select("tr.pncPlayerRow td.playertablePlayerName")[0]


