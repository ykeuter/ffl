from ffl import app, db, models
import requests, re, demjson
from bs4 import BeautifulSoup

DEF_STRING = "D/ST"
FA_STRING = "FA"
NULL_PTS_STRING = "--"

LOGIN_VALUE = "ykeuter@me.com"
PASSWORD = "TP!@8nRZBD2a"

SWID = "{CC149C77-114B-4187-92A1-5F3CBE26117D}"
ESPN_S2 = \
    "AEA7Zo5rL3oSuUsjz7PLUa3wGqx03ZYKZ2g0PhY04qEe2EjQUTevsn%2B6qK6MSUuM%2FUeUkaBJJ5rc55v1%2FPm%2FjQUCzn3n%2FJ4GW2D%2Fp8jM%2BIg2wExHp9AcxrN%2BFMQ6x3f%2FRLGuyT3Af%2BevDgWBj%2BRnVjK17RT9L8WerF%2FS0ZL%2FKtGQWf4r6o9inwnCC7Ankzci7x1s1vIMD%2FQ%2FsJ56cIvNpxV%2F5SuybvQhvYprPseMGWWM8UUjnaMND%2B%2BwFvP67oeMJnX%2FfvuYyQdged576Nq%2B9kni"

LEAGUE_ID = 1427978
TEAM_ID = 6

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

def initDraft():
    url = app.config['DRAFT_INIT_URL'].format(LEAGUE_ID, TEAM_ID, TEAM_ID)
    page = requests.get(url, cookies=dict(SWID=SWID, espn_s2=ESPN_S2))
    soup = BeautifulSoup(page.content, "lxml")
    js = soup.body.find("script").string
    data = re.search(r"var draftleagueData = ({.*?});$", js, re.MULTILINE |
            re.DOTALL).group(1)
    data = demjson.decode(data)
    return data["draftToken"], data["teams"], data["draftOrder"]

def getDraft(token):
    args = token.split(":")
    url = app.config['DRAFT_UPDATE_URL'].format(args[1], args[0], args[1],
            args[2], args[3], token)
    page = requests.get(url, cookies=dict(SWID=SWID, espn_s2=ESPN_S2))
    data = re.search(r'draft.processMessage\(({"token":.*?})\);', page.content)
    data = demjson.decode(data)
    picks = [pick['player']['playerId'] for pick in data['pickHistory']]
    index = data['draftStatus']['currentSelectionId']
    return picks, index
