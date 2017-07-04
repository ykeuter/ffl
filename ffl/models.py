from ffl import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    projected_points = db.Column(db.Float)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    team = db.relationship('Team', backref='players')
    position =  db.relationship('Position', backref='players')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    season_week = db.Column(db.Integer)
    home_team = db.relationship('Team', backref='home_games')
    away_team = db.relationship('Team', backref='away_games')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    bye_week = db.Column(db.Integer)
    projected_defense_points = db.Column(db.Float)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
