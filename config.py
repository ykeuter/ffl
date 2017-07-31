import os

DEBUG = True
SECRET_KEY = 'ro6W6BTzPw29'
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:7tiR9H0NR7Bq@localhost/ffl"
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSITIONS_FILE = "data/positions.csv"
TEAMS_FILE = "data/teams.csv"
PROJECTIONS_FILE = "data/projections.csv"
SCHEDULE_FILE = "data/schedule.csv"
