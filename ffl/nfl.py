from ffl import app, db, models
import requests, re, demjson
from bs4 import BeautifulSoup

URL = "http://www.nfl.com"
BOXSCORE_URL = "http://www.nfl.com/widget/gc/2011/tabs/cat-post-boxscore?gameId={}"

def get_boxscores():
    page = requests.get(URL + "/scores")
    soup = BeautifulSoup(page.content, "lxml")
    years = soup.select("ol.year-selector a")
    for y in years:
        get_boxscore_per_year(y.string)

def get_boxscore_per_year(year):
    page = requests.get(URL + "/scores/{}/REG1".format(year))
    soup = BeautifulSoup(page.content, "lxml")
    weeks = soup.select("a.week-item")
    for w in weeks:
        get_boxscore_per_week(w["href"])
        
def get_boxscore_per_week(week):
    page = requests.get(URL + week)
    soup = BeautifulSoup(page.content, "lxml")
    games = soup.select("div[class='scorebox-wrapper']")
    for g in games:
        print(g.div["id"][9:])

def get_boxscore(id):
    page = requests.get(BOXSCORE_URL.format(id))
    soup = BeautifulSoup(page.content, "lxml")
    teams = [t.a["href"].split("=")[1] for t in
        soup.select("td.team-column-header")]
    # db.session.add(models.NflcomGame(id=int(id),
    #                                  home_team=teams[1],
    #                                  away_team=teams[0]))
    # db.session.commit()
    for (team, table) in zip(teams, soup.select("table.gc-team-leaders-table")):
        row = table.tr
        assert row["class"] == ["thd2"]
        assert row.td.string == "Passing"
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            print(row.td.string)
            # db.session.add(models.NflcomPassing())