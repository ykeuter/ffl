from ffl import app, db, models
import requests
from bs4 import BeautifulSoup

DEF_STRING = "D/ST"
FA_STRING = "FA"
NULL_PTS_STRING = "--"

DRAFT_URL = ""
TEAM_ID = 4

def update_projections():
    teams = models.NflTeam.query.all()
    positions = models.Position.query.all()
    players = models.NflPlayer.query.all()

    for p in players: p.projected_points = None

    url = app.config["PLAYERS_URL"]
    while url:
#        print "Processing " + url + "..."
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")

        playerRows = soup.select("tr.pncPlayerRow")
        for pr in playerRows:
            pts = pr.select("td.appliedPoints")[0].string
            pts = None if pts == NULL_PTS_STRING else float(pts)

            tag = pr.select("td.playertablePlayerName")[0]
            id = int(tag.a["playerid"])
            name = tag.a.string
            details = list(tag.strings)[1].split(None, 2)
            if details[0] == DEF_STRING:
                team = next(x for x in teams if x.espn_id == id)
                team.projected_defense_points = pts
            else:
                if details[1] == FA_STRING: team = None
                else:
                    team = next(x for x in teams
                            if x.espn_code == details[1].upper())
                pos = map(lambda s: next(p for p in positions
                    if s.strip() == p.espn_code), details[2].split(","))
                pl = next((x for x in players if x.espn_id == id), None)
                if pl == None:
                    pl = models.NflPlayer(id, name, team, pos, pts)
                    db.session.add(pl)
                    print "Added player " + name + "."
                    players.append(pl)
                else:
                    pl.name = name
                    pl.team = team
                    pl.positions = pos
                    pl.projected_points = pts
        url = soup.find(string="NEXT")
        if url: url = url.parent["href"]
    db.session.commit()
    print "Updated all projections."

def getDraft():
    teams = models.NflTeam.query.all()
    positions = models.Position.query.all()
    players = models.NflPlayer.query.all()

    for p in players: p.projected_points = None

    url = app.config["PLAYERS_URL"]
    while url:
#        print "Processing " + url + "..."
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")

        playerRows = soup.select("tr.pncPlayerRow")
        for pr in playerRows:
            pts = pr.select("td.appliedPoints")[0].string
            pts = None if pts == NULL_PTS_STRING else float(pts)

            tag = pr.select("td.playertablePlayerName")[0]
            id = int(tag.a["playerid"])
            name = tag.a.string
            details = list(tag.strings)[1].split(None, 2)
            if details[0] == DEF_STRING:
                team = next(x for x in teams if x.espn_id == id)
                team.projected_defense_points = pts
            else:
                if details[1] == FA_STRING: team = None
                else:
                    team = next(x for x in teams
                            if x.espn_code == details[1].upper())
                pos = map(lambda s: next(p for p in positions
                    if s.strip() == p.espn_code), details[2].split(","))
                pl = next((x for x in players if x.espn_id == id), None)
 

