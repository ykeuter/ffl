from ffl import app, db, models
import requests
from csv import DictReader

URL = "https://www.fantasysharks.com/apps/bert/forecasts/projections.php?" \
      "csv=1&Segment={}&Position=99&scoring={}"

def update_projections(segment, scoring):
    teams = models.FieldTeam.query.all()
    url = URL.format(segment, scoring)
    print(url)
    file = requests.get(url)
    print(file.text)
    csv = DictReader(file.text.splitlines())
    for r in csv:
        print(r)
        name = " ".join(reversed(r["Player"].split(", ")))
        team = next(t for t in teams if t.shark_code == r["Team"])
        db.session.add(models.SharkProjections(
            player_name=name, team=team, segment=segment, scoring=scoring,
            points=float(r["Pts"]), position=r["Position"]))

    db.session.commit()
    print("Updated Fantasy Shark projections.")
