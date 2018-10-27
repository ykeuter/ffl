from ffl import app, db, models
import requests, datetime, stringcase

SEASON_URL = 'https://api.nfl.com/v3/shield/?' \
    'query=query{{viewer{{season(season:{})' \
    '{{weeks{{id games{{id esbId gameDetailId gameTime networkChannels ' \
    'venue{{city state displayName}}awayTeam{{nickName id abbreviation ' \
    'logo{{permalink}}injuries{{leagueReportedInjuries{{playerId}}}}}}' \
    'homeTeam{{nickName id abbreviation logo{{permalink}}' \
    'injuries{{leagueReportedInjuries{{playerId}}}}}}}}season{{id}}' \
    'weekOrder seasonType seasonValue weekOrder weekType weekValue}}}}}}}}&' \
    'variables=null'

PLAYER_GAME_STATS_URL = 'https://api.nfl.com/v3/shield/?' \
    'query=query{{viewer{{playerGameStats(first:200,game_id:"{}")' \
    '{{edges{{cursor node{{createdDate game{{id}}gameStats{{' \
    'defensiveAssists defensiveInterceptions defensiveInterceptionsYards ' \
    'defensiveForcedFumble defensivePassesDefensed defensiveSacks ' \
    'defensiveSafeties defensiveSoloTackles defensiveTotalTackles ' \
    'defensiveTacklesForALoss touchdownsDefense fumblesLost fumblesTotal ' \
    'kickReturns kickReturnsLong kickReturnsTouchdowns kickReturnsYards ' \
    'kickingFgAtt kickingFgLong kickingFgMade kickingXkAtt kickingXkMade ' \
    'passingAttempts passingCompletions passingTouchdowns passingYards ' \
    'passingInterceptions puntReturns puntingAverageYards puntingLong ' \
    'puntingPunts puntingPuntsInside20 receivingReceptions receivingTarget ' \
    'receivingTouchdowns receivingYards rushingAttempts rushingAverageYards ' \
    'rushingTouchdowns rushingYards kickoffReturnsTouchdowns ' \
    'kickoffReturnsYards puntReturnsLong opponentFumbleRecovery ' \
    'totalPointsScored kickReturnsAverageYards puntReturnsAverageYards ' \
    'puntReturnsTouchdowns}}id lastModifiedDate player{{position ' \
    'jerseyNumber currentTeam{{abbreviation nickName}}person{{firstName ' \
    'lastName displayName id headshot{{asset{{url}}}}}}}}' \
    'season{{id}}week{{id}}}}}}}}}}}}&' \
    'variables=null'

LIVE_URL = 'https://api.nfl.com/v3/shield/?' \
    'query=query{{viewer{{live{{playerGameStats(gameDetailId:"{}")' \
    '{{createdDate gameStats{{defensiveAssists defensiveInterceptions ' \
    'defensiveInterceptionsYards defensiveForcedFumble ' \
    'defensivePassesDefensed defensiveSacks defensiveSafeties ' \
    'defensiveSoloTackles defensiveTotalTackles defensiveTacklesForALoss ' \
    'touchdownsDefense fumblesLost fumblesTotal kickReturns kickReturnsLong ' \
    'kickReturnsTouchdowns kickReturnsYards kickingFgAtt kickingFgLong ' \
    'kickingFgMade kickingXkAtt kickingXkMade passingAttempts ' \
    'passingCompletions passingTouchdowns passingYards passingInterceptions ' \
    'puntReturns puntingAverageYards puntingLong puntingPunts ' \
    'puntingPuntsInside20 receivingReceptions receivingTarget ' \
    'receivingTouchdowns receivingYards rushingAttempts rushingAverageYards ' \
    'rushingTouchdowns rushingYards kickoffReturnsTouchdowns ' \
    'kickoffReturnsYards puntReturnsLong opponentFumbleRecovery ' \
    'totalPointsScored kickReturnsAverageYards puntReturnsAverageYards ' \
    'puntReturnsTouchdowns}}lastModifiedDate team{{nickName abbreviation}}' \
    'player{{id position firstName nickName lastName}}}}}}}}}}&' \
    'variables=null'

TOKEN_URL = "https://api.nfl.com/v1/reroute"

PLAYER_GAME_STATS = [
    'defensive_assists',
    'defensive_interceptions',
    'defensive_interceptions_yards',
    'defensive_forced_fumble',
    'defensive_passes_defensed',
    'defensive_sacks',
    'defensive_safeties',
    'defensive_solo_tackles',
    'defensive_total_tackles',
    'defensive_tackles_for_a_loss',
    'touchdowns_defense',
    'fumbles_lost',
    'fumbles_total',
    'kick_returns',
    'kick_returns_long',
    'kick_returns_touchdowns',
    'kick_returns_yards',
    'kicking_fg_att',
    'kicking_fg_long',
    'kicking_fg_made',
    'kicking_xk_att',
    'kicking_xk_made',
    'passing_attempts',
    'passing_completions',
    'passing_touchdowns',
    'passing_yards',
    'passing_interceptions',
    'punt_returns',
    'punting_average_yards',
    'punting_long',
    'punting_punts',
    'punting_punts_inside20',
    'receiving_receptions',
    'receiving_target',
    'receiving_touchdowns',
    'receiving_yards',
    'rushing_attempts',
    'rushing_average_yards',
    'rushing_touchdowns',
    'rushing_yards',
    'kickoff_returns_touchdowns',
    'kickoff_returns_yards',
    'punt_returns_long',
    'opponent_fumble_recovery',
    'total_points_scored',
    'kick_returns_average_yards',
    'punt_returns_average_yards',
    'punt_returns_touchdowns',
]

def get_token():
    data = {"grant_type": "client_credentials"}
    headers = {"x-domain-id": "100"}
    r = requests.post(TOKEN_URL, data=data, headers=headers).json()
    return r['access_token']

def load_boxscores():
    START = 2010
    token = get_token()
    for y in range(START, datetime.datetime.now().year):
        load_boxscores_per_year(y, token=token)

def load_live_boxscore(detail_id, token=None):
    if token is None:
        token = get_token()
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get(LIVE_URL.format(detail_id), headers=headers).json()
    edges = r['data']['viewer']['live']['playerGameStats']
    if len(edges) == 0:
        print("EMPTY LIVE: {}".format(detail_id))
    for e in edges:
        stats = {s: e['gameStats'][stringcase.camelcase(s)]
                 for s in PLAYER_GAME_STATS}
        if sum(x for x in stats.values() if x is not None):
            stats.update({
                "game_detail_id": detail_id,
                "team_abbr": e['team']['abbreviation'],
                "person_id": e['player']['id'],
                "person_name":
                    "{} {}".format(e['player']['firstName'],
                                   e['player']['lastName'])})
            db.session.add(models.NflLivePlayerGameStats(**stats))
    db.session.commit()

def load_boxscores_per_year(year, week=None, token=None):
    if token is None:
        token = get_token()
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get(SEASON_URL.format(year), headers=headers).json()
    weeks = r['data']['viewer']['season']['weeks']
    if week is not None:
        weeks = [w for w in weeks if w['weekOrder'] == week]
    for w in weeks:
        print("year: {}, week: {}".format(w['seasonValue'], w['weekOrder']))
        game = {"week_order": w['weekOrder'],
                "week_value": w['weekValue'],
                "week_type": w['weekType'],
                "season_value": w['seasonValue'],
                "season_type": w['seasonType']}
        for g in w['games']:
            game.update({"id": g['id'],
                         "detail_id": g['gameDetailId'],
                         "home_team_id": g['homeTeam']['id'],
                         "away_team_id": g['awayTeam']['id'],
                         "home_team_abbr": g['homeTeam']['abbreviation'],
                         "away_team_abbr": g['awayTeam']['abbreviation']})
            db.session.add(models.NflGame(**game))
            db.session.commit()
            load_boxscore(g['id'], token)
            load_live_boxscore(g['gameDetailId'], token)

def load_boxscore(id, token=None):
    if token is None:
        token = get_token()
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get(PLAYER_GAME_STATS_URL.format(id), headers=headers).json()
    edges = r['data']['viewer']['playerGameStats']['edges']
    if len(edges) == 0:
        print("EMPTY: {}".format(id))
    for e in edges:
        stats = {s: e['node']['gameStats'][stringcase.camelcase(s)]
                 for s in PLAYER_GAME_STATS}
        if sum(x for x in stats.values() if x is not None):
            stats.update({
                "game_id": e['node']['game']['id'],
                "team_abbr": e['node']['player']['currentTeam']['abbreviation'],
                "person_id": e['node']['player']['person']['id'],
                "person_name": e['node']['player']['person']['displayName']})
            db.session.add(models.NflPlayerGameStats(**stats))
    db.session.commit()
