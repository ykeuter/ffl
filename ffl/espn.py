from ffl import app, db, models
import requests, re, demjson
from bs4 import BeautifulSoup

DEF_STRING = "D/ST"
FA_STRING = "FA"
NULL_PTS_STRING = "--"

SWID = app.config['SWID']
ESPN_S2 = app.config['ESPN_S2']

LEAGUE_ID = app.config['LEAGUE_ID']
TEAM_ID = app.config['TEAM_ID']

def update_projections():
    teams = models.NflTeam.query.all()
    positions = models.Position.query.all()
    players = models.NflPlayer.query.all()

    for p in players: p.projected_points = None

    url = app.config["PLAYERS_URL"].format(LEAGUE_ID)
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
                pos = [next(p for p in positions if s.strip() == p.espn_code)
                    for s in details[2].split(",")]
                pl = next((x for x in players if x.espn_id == id), None)
                if pl == None:
                    pl = models.NflPlayer(id, name, team, pos, pts)
                    db.session.add(pl)
                    print("Added player " + name + ".")
                    players.append(pl)
                else:
                    pl.name = name
                    pl.team = team
                    pl.positions = pos
                    pl.projected_points = pts
        url = soup.find(string="NEXT")
        if url: url = url.parent["href"]
    db.session.commit()
    print("Updated all projections.")

def initDraft():
    url = app.config['DRAFT_INIT_URL'].format(LEAGUE_ID, TEAM_ID, TEAM_ID)
    page = requests.get(url, cookies=dict(SWID=SWID, espn_s2=ESPN_S2))
    soup = BeautifulSoup(page.text, "lxml")
    js = soup.body.find("script").string
    data = re.search(r"var draftleagueData = ({.*?});$", js, re.MULTILINE |
            re.DOTALL).group(1)
    data = demjson.decode(data)
    return data["draftToken"], data["teams"], [x -  1 for x in
            data["draftOrder"]]

def getDraft(token):
    args = token.split(":")
    url = app.config['DRAFT_UPDATE_URL'].format(args[1], args[0], args[1],
            args[2], args[3], token)
    page = requests.get(url, cookies=dict(SWID=SWID, espn_s2=ESPN_S2))
    data = re.search(r'draft.processMessage\(({"token":.*?})\);',
            page.text).group(1)
    data = demjson.decode(data)
    picks = [{'playerId': pick['player']['playerId'],
        'teamId': pick['teamId'] - 1} for pick in data['pickHistory']]
    index = data['draftStatus']['currentSelectionId']
    return picks, index
