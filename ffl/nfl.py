from ffl import app, db, models
import requests, re, demjson
from bs4 import BeautifulSoup

URL = "http://www.nfl.com/scores"
BOXSCORE_URL = "http://www.nfl.com/widget/gc/2011/tabs/cat-post-boxscore?gameId={}"

def load_boxscores():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
    years = soup.select("ol.year-selector a")
    for y in years:
        load_boxscores_per_year(int(y.string))

def load_boxscores_per_year(year):
    page = requests.get(URL + "/{}/REG1".format(year))
    soup = BeautifulSoup(page.content, "lxml")
    weeks = soup.select("a.week-item")
    for w in weeks:
        load_boxscores_per_week(year, w["href"].split("/")[-1])
        
def load_boxscores_per_week(year, week):
    page = requests.get(URL + "/{}/{}".format(year, week))
    soup = BeautifulSoup(page.content, "lxml")
    games = soup.select("div[class='scorebox-wrapper']")
    for g in games:
        load_boxscore(year, week, int(g.div["id"][9:]))

def load_boxscore(year, week, id):
    print("Loading game {}...".format(id))
    page = requests.get(BOXSCORE_URL.format(id))
    soup = BeautifulSoup(page.content, "lxml")
    teams = [t.a["href"].split("=")[1] for t in
        soup.select("td.team-column-header")]
    db.session.add(models.NflBoxscoreGame(id=id, year=year, week=week,
                                          home_team=teams[1],
                                          away_team=teams[0]))
    db.session.commit()
    for (team, table) in zip(teams, soup.select("table.gc-team-leaders-table")):
        row = table.tr
        assert row["class"] == ["thd2"]
        
        # Passing
        cols = ["Passing", "CP/AT", "YDS", "TD", "INT"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["cp"], d["at"] = [int(x) for x in cols[1].string.split("/")]
            d["yds"] = int(cols[2].string)
            d["td"] = int(cols[3].string)
            d["int"] = int(cols[4].string)
            db.session.add(models.NflBoxscorePassing(**d))

        # Rushing
        cols = ["Rushing", "ATT", "YDS", "TD", "LG"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["att"] = int(cols[1].string)
            d["yds"] = int(cols[2].string)
            d["td"] = int(cols[3].string)
            if cols[4].string[-1] == "T":
                d["lg_td"] = True
                d["lg"] = int(cols[4].string[:-1])
            else:
                d["lg_td"] = False
                d["lg"] = int(cols[4].string)
            db.session.add(models.NflBoxscoreRushing(**d))

        # Receiving
        cols = ["Receiving", "REC", "YDS", "TD", "LG"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["rec"] = int(cols[1].string)
            d["yds"] = int(cols[2].string)
            d["td"] = int(cols[3].string)
            if cols[4].string[-1] == "T":
                d["lg_td"] = True
                d["lg"] = int(cols[4].string[:-1])
            else:
                d["lg_td"] = False
                d["lg"] = int(cols[4].string)
            db.session.add(models.NflBoxscoreReceiving(**d))

        # Fumbles
        cols = ["Fumbles", "FUM", "LOST", "REC", "YDS"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["fum"] = int(cols[1].string)
            d["lost"] = int(cols[2].string)
            d["rec"] = int(cols[3].string)
            d["yds"] = int(cols[4].string)
            db.session.add(models.NflBoxscoreFumbles(**d))

        # Kicking
        cols = ["Kicking", "FG", "LG", "XP", "PTS"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["fg_att"], d["fg_made"] = \
                [int(x) for x in cols[1].string.split("/")]
            d["lg"] = int(cols[2].string)
            d["xp_att"], d["xp_made"] = \
                [int(x) for x in cols[3].string.split("/")]
            d["pts"] = int(cols[4].string)
            db.session.add(models.NflBoxscoreKicking(**d))

        # Punting
        cols = ["Punting", "NO", "AVG", "I20", "LG"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["no"] = int(cols[1].string)
            d["avg"] = float(cols[2].string)
            d["i20"] = int(cols[3].string)
            d["lg"] = int(cols[4].string)
            db.session.add(models.NflBoxscorePunting(**d))

        # Kickoff Returns
        cols = ["Kickoff Returns", "NO", "AVG", "TD", "LG"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["no"] = int(cols[1].string)
            d["avg"] = int(cols[2].string)
            d["td"] = int(cols[3].string)
            d["lg"] = int(cols[4].string)
            db.session.add(models.NflBoxscoreKickoffReturns(**d))

        # Punt Returns
        cols = ["Punt Returns", "NO", "AVG", "TD", "LG"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["no"] = int(cols[1].string)
            d["avg"] = int(cols[2].string)
            d["td"] = int(cols[3].string)
            if cols[4].string[-1] == "T":
                d["lg_td"] = True
                d["lg"] = int(cols[4].string[:-1])
            else:
                d["lg_td"] = False
                d["lg"] = int(cols[4].string)
            db.session.add(models.NflBoxscorePuntReturns(**d))

        # Defense
        cols = ["Defense", "T-A", "SCK", "INT", "FF"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row is None: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["t"], d["a"] = \
                [int(x) for x in cols[1].string.split("-")]
            d["sck"] = float(cols[2].string)
            d["int"] = int(cols[3].string)
            d["ff"] = int(cols[4].string)
            db.session.add(models.NflBoxscoreDefense(**d))

    db.session.commit()