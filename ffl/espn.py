from ffl import app, db, models
import requests, re, demjson
from bs4 import BeautifulSoup

DEF_STRING = "D/ST"
FA_STRING = "FA"
NULL_PTS_STRING = "--"

SWID = app.config['ESPN_SWID']
ESPN_S2 = app.config['ESPN_S2']

LEAGUE_ID = app.config['ESPN_LEAGUE_ID']
TEAM_ID = app.config['ESPN_TEAM_ID']

PLAYERS_URL = "http://games.espn.com/ffl/tools/projections?leagueId={}"
DRAFT_INIT_URL = \
    "http://games.espn.com/ffl/htmldraft?leagueId={}&teamId={}&fromTeamId={}"
DRAFT_UPDATE_URL = \
    "http://ffl.draft.espn.com/league-{}/extdraft/json/JOIN?" \
    "1={}&2={}&3={}&4={}&5={}&poll=0"

def update_projections(league_id):
    models.EspnProjections.query.filter_by(league_id=int(league_id)).delete()
    db.session.commit()
    teams = models.FieldTeam.query.all()
    ids = [p.espn_id for p in models.FieldPlayer.query.all()]
    url = PLAYERS_URL.format(league_id)
    while url:
#        print "Processing " + url + "..."
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")

        playerRows = soup.select("tr.pncPlayerRow")
        for pr in playerRows:
            pts = pr.select("td.appliedPoints")[0].string
            pts = None if pts == NULL_PTS_STRING else float(pts)

            st = pr.select("td")[1].string

            tag = pr.select("td.playertablePlayerName")[0]
            id_ = int(tag.a["playerid"])
            name = tag.a.string
            if id_ not in ids:
                db.session.add(models.FieldPlayer(espn_id=id_, name=name))
            details = list(tag.strings)[1].split(None, 2)
            if details[0] == DEF_STRING:
                team = next(t for t in teams if t.espn_id == id_)
                pos = [details[0]]
            else:
                if details[1] == FA_STRING:
                    team = None
                else:
                    team = next(t for t in teams
                                if t.espn_code == details[1].upper())
                pos = [s.strip() for s in details[2].split(",")]

            db.session.add(models.EspnProjections(
                player_id=id_, player_name=name, team=team,
                points=pts, league_id=league_id, positions=pos, status=st))

        url = soup.find(string="NEXT")
        if url: url = url.parent["href"]
    db.session.commit()
    print("Updated ESPN projections for league {}.".format(league_id))

def initDraft():
    url = DRAFT_INIT_URL.format(LEAGUE_ID, TEAM_ID, TEAM_ID)
    page = requests.get(url, cookies=dict(SWID=SWID, espn_s2=ESPN_S2))
    soup = BeautifulSoup(page.text, "lxml")
    js = soup.body.find("script").string
    data = re.search(r"var draftleagueData = ({.*?});$", js, re.MULTILINE |
            re.DOTALL).group(1)
    data = demjson.decode(data)
    return data["draftToken"], data["teams"], data["draftOrder"]

def getDraft(token):
    args = token.split(":")
    url = DRAFT_UPDATE_URL.format(args[1], args[0], args[1],
            args[2], args[3], token)
    page = requests.get(url, cookies=dict(SWID=SWID, espn_s2=ESPN_S2))
    data = re.search(r'draft.processMessage\(({"token":.*?})\);',
            page.text).group(1)
    data = demjson.decode(data)
    picks = [{'playerId': pick['player']['playerId'],
        'teamId': pick['teamId']} for pick in data['pickHistory']]
    index = data['draftStatus']['currentSelectionId']
    return picks, index
