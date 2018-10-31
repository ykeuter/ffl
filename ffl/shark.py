from ffl import db, models
import requests
from bs4 import BeautifulSoup

RET_STRING = "Ret"
SANITY_POS = ["QB", "RB", "WR", "TE", "D", "K"]

URL = "https://www.fantasysharks.com/apps/bert/forecasts/projections.php?" \
      "Segment={}&Position=99&scoring={}"

def update_projections(segment, scoring):
    teams = models.FieldTeam.query.all()
    ids = [p.shark_id for p in models.FieldPlayer.query.all()]

    url = URL.format(segment, scoring)
    page = requests.get(url, headers={"user-agent": None})
    soup = BeautifulSoup(page.content, "lxml").select_one("div.toolDiv")
    pos_idx = list(soup.tr.strings).index("Position")
    for r in soup.select("tr"):
        cols = r.select("td")
        if len(cols) < 2 or cols[2].string == RET_STRING:
            continue
        id_ = int(cols[1].a["href"].split("=")[-1])
        name = " ".join(reversed(cols[1].a.string.split(", ")))
        if id_ not in ids:
            db.session.add(models.FieldPlayer(shark_id=id_, name=name))
        team = next(t for t in teams if t.shark_code == cols[2].string)
        pos = cols[pos_idx].string
        pts = float(cols[-1].string)
        db.session.add(models.SharkProjections(
            player_id = id_, player_name=name, team=team, segment=segment,
            scoring=scoring,points=pts, position=pos))

    db.session.commit()
    print("Updated Fantasy Shark projections.")
    check_sanity()

def check_sanity():
    players = {s.player for s in models.SharkProjections.query.all()
               if s.player.espn_id is None and s.position in SANITY_POS}
    for p in players:
        print("Missing ESPN player for {} ({}).".format(p.name, p.shark_id))
