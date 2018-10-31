import os
from dotenv import load_dotenv

load_dotenv()

# DEBUG = True
SECRET_KEY = 'ro6W6BTzPw29'
SQLALCHEMY_DATABASE_URI = os.environ['FFL_DB_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSITIONS_FILE = "data/positions.csv"
TEAMS_FILE = "data/teams.csv"
PLAYERS_FILE = "data/players.csv"
#PROJECTIONS_FILE = "data/projections.csv"
#SCHEDULE_FILE = "data/schedule.csv"
# ESPN_LOGIN_URL = \
#     "https://ha.registerdisney.go.com/jgc/v5/client/ESPN-ESPNCOM-PROD/guest/login?langPref=en-US"
# ESPN_APIKEY_URL = \
#     "https://registerdisney.go.com/jgc/v5/client/ESPN-ESPNCOM-PROD/api-key?langPref=en-US"
ESPN_TEAM_ID = os.environ['FFL_TEAM_ID']
ESPN_LEAGUE_ID = os.environ['FFL_LEAGUE_ID']
ESPN_SWID = os.environ['FFL_SWID']
ESPN_S2 = os.environ['FFL_ESPN_S2']
ITERMAX = os.environ['FFL_ITERMAX']
SHARK_SCORING = os.environ['FFL_SHARK_SCORING']
SHARK_SEGMENT = os.environ['FFL_SHARK_SEGMENT']
