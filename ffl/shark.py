from ffl import db, models
import requests
from bs4 import BeautifulSoup

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
        if len(cols) < 2:
            continue
        id_ = int(cols[1].a["href"].split("=")[-1])
        if id_ not in ids:
            db.session.add(models.FieldPlayer(shark_id=id_))
        name = " ".join(reversed(cols[1].a.string.split(", ")))
        team = next(t for t in teams if t.shark_code == cols[2].string)
        pos = cols[pos_idx].string
        pts = float(cols[-1].string)
        db.session.add(models.SharkProjections(
            player_id = id_, player_name=name, team=team, segment=segment,
            scoring=scoring,points=pts, position=pos))

    db.session.commit()
    print("Updated Fantasy Shark projections.")
