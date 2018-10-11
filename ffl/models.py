from ffl import db

playerPosition = db.Table('nfl_player_position',
        db.Column('player_id', db.Integer, db.ForeignKey('nfl_player.id')),
        db.Column('posiiton_id', db.Integer, db.ForeignKey('position.id')))

class NflBoxscoreGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    week = db.Column(db.String(32))
    home_team = db.Column(db.String(32))
    away_team = db.Column(db.String(32))

class NflBoxscorePassing(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    cp = db.Column(db.Integer)
    at = db.Column(db.Integer)
    yds = db.Column(db.Integer)
    td = db.Column(db.Integer)
    int = db.Column(db.Integer)
    team = db.Column(db.String(32))

class NflBoxscoreRushing(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    att = db.Column(db.Integer)
    yds = db.Column(db.Integer)
    td = db.Column(db.Integer)
    lg = db.Column(db.Integer)
    lg_td = db.Column(db.Boolean)
    team = db.Column(db.String(32))

class NflBoxscoreReceiving(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    rec = db.Column(db.Integer)
    yds = db.Column(db.Integer)
    td = db.Column(db.Integer)
    lg = db.Column(db.Integer)
    lg_td = db.Column(db.Boolean)
    team = db.Column(db.String(32))

class NflBoxscoreFumbles(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    fum = db.Column(db.Integer)
    lost = db.Column(db.Integer)
    rec = db.Column(db.Integer)
    yds = db.Column(db.Integer)
    team = db.Column(db.String(32))

class NflBoxscoreKicking(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    fg_att = db.Column(db.Integer)
    fg_made = db.Column(db.Integer)
    lg = db.Column(db.Integer)
    xp_att = db.Column(db.Integer)
    xp_made = db.Column(db.Integer)
    pts = db.Column(db.Integer)
    team = db.Column(db.String(32))

class NflBoxscorePunting(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    no = db.Column(db.Integer)
    avg = db.Column(db.Float)
    i20 = db.Column(db.Integer)
    lg = db.Column(db.Integer)
    team = db.Column(db.String(32))

class NflBoxscoreKickoffReturns(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    no = db.Column(db.Integer)
    avg = db.Column(db.Integer)
    td = db.Column(db.Integer)
    lg = db.Column(db.Integer)
    team = db.Column(db.String(32))

class NflBoxscorePuntReturns(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    no = db.Column(db.Integer)
    avg = db.Column(db.Integer)
    td = db.Column(db.Integer)
    lg = db.Column(db.Integer)
    lg_td = db.Column(db.Boolean)
    team = db.Column(db.String(32))

class NflBoxscoreDefense(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('nfl_boxscore_game.id',
                                                  ondelete="CASCADE"),
                        primary_key=True)
    player_id = db.Column(db.String(32), primary_key=True)
    player_name = db.Column(db.String(32))
    t = db.Column(db.Integer)
    a = db.Column(db.Integer)
    sck = db.Column(db.Float)
    int = db.Column(db.Integer)
    ff = db.Column(db.Integer)
    team = db.Column(db.String(32))

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

class NflGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('nfl_team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('nfl_team.id'))
    season_week = db.Column(db.Integer)
    home_team = db.relationship('NflTeam', backref='home_games',
            foreign_keys=[home_team_id])
    away_team = db.relationship('NflTeam', backref='away_games',
            foreign_keys=[away_team_id])

    def __init__(self, homeTeam, awayTeam, seasonWeek):
        self.home_team = homeTeam
        self.away_team = awayTeam
        self.season_week = seasonWeek

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

class PlayerGameStats(db.Model):
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