from ffl import db
from sqlalchemy.dialects.postgresql import ARRAY

playerPosition = db.Table('nfl_player_position',
        db.Column('player_id', db.Integer, db.ForeignKey('nfl_player.id')),
        db.Column('posiiton_id', db.Integer, db.ForeignKey('position.id')))

class SharkProjections(db.Model):
    segment = db.Column(db.Integer, primary_key=True)
    scoring = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('field_player.shark_id'),
                          primary_key=True)
    player_name = db.Column(db.String(64))
    team_id = db.Column(db.Integer, db.ForeignKey('field_team.id'))
    position = db.Column(db.String(8))
    points = db.Column(db.Float)
    team = db.relationship('FieldTeam', backref='shark_projections')

class EspnProjections(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('field_player.espn_id'),
                          primary_key=True)
    league_id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(64))
    team_id = db.Column(db.Integer, db.ForeignKey('field_team.id'))
    points = db.Column(db.Float)
    positions =  db.Column(ARRAY(db.String(8)))
    status = db.Column(db.String(32))
    team = db.relationship('FieldTeam', backref='espn_projections')

class FieldPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    espn_id = db.Column(db.Integer, unique=True)
    shark_id = db.Column(db.Integer, unique=True)

class FieldTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    espn_code = db.Column(db.String(8))
    espn_id = db.Column(db.Integer)
    shark_code = db.Column(db.String(8))

class NflGame(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    detail_id = db.Column(db.String(64), unique=True)
    season_value = db.Column(db.Integer)
    season_type = db.Column(db.String(32))
    week_order = db.Column(db.Integer)
    week_value = db.Column(db.Integer)
    week_type = db.Column(db.String(32))
    home_team_id = db.Column(db.String(64))
    away_team_id = db.Column(db.String(64))
    home_team_abbr = db.Column(db.String(32))
    away_team_abbr = db.Column(db.String(32))

class NflPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    espn_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    team_id = db.Column(db.Integer, db.ForeignKey('nfl_team.id'))
    projected_points = db.Column(db.Float)
    team = db.relationship('NflTeam', backref='players')
    positions =  db.relationship('Position', secondary=playerPosition,
            backref='players')

    def __init__(self, id, name, team, positions, points):
        self.espn_id = id
        self.name = name
        self.team = team
        self.positions = positions
        self.projected_points = points

class NflTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    espn_code = db.Column(db.String(32))
    espn_id = db.Column(db.Integer)
    bye_week = db.Column(db.Integer)
    projected_defense_points = db.Column(db.Float)

    def __init__(self, id, code, name):
        self.espn_id = id
        self.espn_code = code
        self.name = name

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    espn_code = db.Column(db.String(8))
    name = db.Column(db.String(32))
    order = db.Column(db.Integer)

class UserEmail(db.Model):
    email = db.Column(db.String(128), primary_key=True)

class NflPlayerGameStats(db.Model):
    game_id = db.Column(db.String(64),
                        db.ForeignKey('nfl_game.id', ondelete="CASCADE"),
                        primary_key=True)
    team_abbr = db.Column(db.String(32))
    person_name = db.Column(db.String(128))
    person_id = db.Column(db.String(64), primary_key=True)

    defensive_assists = db.Column(db.Float)
    defensive_interceptions = db.Column(db.Float)
    defensive_interceptions_yards = db.Column(db.Float)
    defensive_forced_fumble = db.Column(db.Float)
    defensive_passes_defensed = db.Column(db.Float)
    defensive_sacks = db.Column(db.Float)
    defensive_safeties = db.Column(db.Float)
    defensive_solo_tackles = db.Column(db.Float)
    defensive_total_tackles = db.Column(db.Float)
    defensive_tackles_for_a_loss = db.Column(db.Float)
    touchdowns_defense = db.Column(db.Float)
    fumbles_lost = db.Column(db.Float)
    fumbles_total = db.Column(db.Float)
    kick_returns = db.Column(db.Float)
    kick_returns_long = db.Column(db.Float)
    kick_returns_touchdowns = db.Column(db.Float)
    kick_returns_yards = db.Column(db.Float)
    kicking_fg_att = db.Column(db.Float)
    kicking_fg_long = db.Column(db.Float)
    kicking_fg_made = db.Column(db.Float)
    kicking_xk_att = db.Column(db.Float)
    kicking_xk_made = db.Column(db.Float)
    passing_attempts = db.Column(db.Float)
    passing_completions = db.Column(db.Float)
    passing_touchdowns = db.Column(db.Float)
    passing_yards = db.Column(db.Float)
    passing_interceptions = db.Column(db.Float)
    punt_returns = db.Column(db.Float)
    punting_average_yards = db.Column(db.Float)
    punting_long = db.Column(db.Float)
    punting_punts = db.Column(db.Float)
    punting_punts_inside20 = db.Column(db.Float)
    receiving_receptions = db.Column(db.Float)
    receiving_target = db.Column(db.Float)
    receiving_touchdowns = db.Column(db.Float)
    receiving_yards = db.Column(db.Float)
    rushing_attempts = db.Column(db.Float)
    rushing_average_yards = db.Column(db.Float)
    rushing_touchdowns = db.Column(db.Float)
    rushing_yards = db.Column(db.Float)
    kickoff_returns_touchdowns = db.Column(db.Float)
    kickoff_returns_yards = db.Column(db.Float)
    punt_returns_long = db.Column(db.Float)
    opponent_fumble_recovery = db.Column(db.Float)
    total_points_scored = db.Column(db.Float)
    kick_returns_average_yards = db.Column(db.Float)
    punt_returns_average_yards = db.Column(db.Float)
    punt_returns_touchdowns = db.Column(db.Float)

class NflLivePlayerGameStats(db.Model):
    game_detail_id = db.Column(db.String(64),
                        db.ForeignKey('nfl_game.detail_id',
                                      ondelete="CASCADE"),
                        primary_key=True)
    team_abbr = db.Column(db.String(32))
    person_name = db.Column(db.String(128))
    person_id = db.Column(db.String(64), primary_key=True)

    defensive_assists = db.Column(db.Float)
    defensive_interceptions = db.Column(db.Float)
    defensive_interceptions_yards = db.Column(db.Float)
    defensive_forced_fumble = db.Column(db.Float)
    defensive_passes_defensed = db.Column(db.Float)
    defensive_sacks = db.Column(db.Float)
    defensive_safeties = db.Column(db.Float)
    defensive_solo_tackles = db.Column(db.Float)
    defensive_total_tackles = db.Column(db.Float)
    defensive_tackles_for_a_loss = db.Column(db.Float)
    touchdowns_defense = db.Column(db.Float)
    fumbles_lost = db.Column(db.Float)
    fumbles_total = db.Column(db.Float)
    kick_returns = db.Column(db.Float)
    kick_returns_long = db.Column(db.Float)
    kick_returns_touchdowns = db.Column(db.Float)
    kick_returns_yards = db.Column(db.Float)
    kicking_fg_att = db.Column(db.Float)
    kicking_fg_long = db.Column(db.Float)
    kicking_fg_made = db.Column(db.Float)
    kicking_xk_att = db.Column(db.Float)
    kicking_xk_made = db.Column(db.Float)
    passing_attempts = db.Column(db.Float)
    passing_completions = db.Column(db.Float)
    passing_touchdowns = db.Column(db.Float)
    passing_yards = db.Column(db.Float)
    passing_interceptions = db.Column(db.Float)
    punt_returns = db.Column(db.Float)
    punting_average_yards = db.Column(db.Float)
    punting_long = db.Column(db.Float)
    punting_punts = db.Column(db.Float)
    punting_punts_inside20 = db.Column(db.Float)
    receiving_receptions = db.Column(db.Float)
    receiving_target = db.Column(db.Float)
    receiving_touchdowns = db.Column(db.Float)
    receiving_yards = db.Column(db.Float)
    rushing_attempts = db.Column(db.Float)
    rushing_average_yards = db.Column(db.Float)
    rushing_touchdowns = db.Column(db.Float)
    rushing_yards = db.Column(db.Float)
    kickoff_returns_touchdowns = db.Column(db.Float)
    kickoff_returns_yards = db.Column(db.Float)
    punt_returns_long = db.Column(db.Float)
    opponent_fumble_recovery = db.Column(db.Float)
    total_points_scored = db.Column(db.Float)
    kick_returns_average_yards = db.Column(db.Float)
    punt_returns_average_yards = db.Column(db.Float)
    punt_returns_touchdowns = db.Column(db.Float)
