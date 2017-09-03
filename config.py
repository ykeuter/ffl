import os

# DEBUG = True
SECRET_KEY = 'ro6W6BTzPw29'
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:7tiR9H0NR7Bq@localhost/ffl"
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSITIONS_FILE = "data/positions.csv"
TEAMS_FILE = "data/teams.csv"
#PROJECTIONS_FILE = "data/projections.csv"
PLAYERS_URL = "http://games.espn.com/ffl/tools/projections?leagueId=438192"
SCHEDULE_FILE = "data/schedule.csv"
DRAFT_INIT_URL = \
    "http://games.espn.com/ffl/htmldraft?leagueId={}&teamId={}&fromTeamId={}"
DRAFT_UPDATE_URL = \
    "http://ffl.draft.espn.com/league-{}/extdraft/json/JOIN?1={}&2={}&3={}&4={}&5={}&poll=0"
ESPN_LOGIN_URL = \
    "https://ha.registerdisney.go.com/jgc/v5/client/ESPN-ESPNCOM-PROD/guest/login?langPref=en-US"
ESPN_APIKEY_URL = \
    "https://registerdisney.go.com/jgc/v5/client/ESPN-ESPNCOM-PROD/api-key?langPref=en-US"
