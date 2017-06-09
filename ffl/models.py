from ffl.app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.
class Team(db.MOdel):


