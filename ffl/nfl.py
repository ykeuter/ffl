from ffl import app, db, models
import requests, re, demjson
from bs4 import BeautifulSoup

SEASON_URL = "https://api.nfl.com/v3/shield/?" \
    "query=query{viewer{season(season:{})" \
    "{weeks{id games{id esbId gameDetailId gameTime networkChannels " \
    "venue{city state displayName}awayTeam{nickName id abbreviation " \
    "logo{permalink}injuries{leagueReportedInjuries{playerId}}}" \
    "homeTeam{nickName id abbreviation logo{permalink}" \
    "injuries{leagueReportedInjuries{playerId}}}}season{id}weekOrder " \
    "seasonType seasonValue weekOrder weekType weekValue}}}}&" \
    "variables=null"

PLAYER_GAME_STATS_URL = "https://api.nfl.com/v3/shield/?" \
    "query=query{viewer{playerGameStats(first:200,game_id:"{}")" \
    "{edges{cursor node{createdDate game{id}gameStats{defensiveAssists " \
    "defensiveInterceptions defensiveInterceptionsYards " \
    "defensiveForcedFumble defensivePassesDefensed defensiveSacks " \
    "defensiveSafeties defensiveSoloTackles defensiveTotalTackles " \
    "defensiveTacklesForALoss touchdownsDefense fumblesLost fumblesTotal " \
    "kickReturns kickReturnsLong kickReturnsTouchdowns kickReturnsYards " \
    "kickingFgAtt kickingFgLong kickingFgMade kickingXkAtt kickingXkMade " \
    "passingAttempts passingCompletions passingTouchdowns passingYards " \
    "passingInterceptions puntReturns puntingAverageYards puntingLong " \
    "puntingPunts puntingPuntsInside20 receivingReceptions receivingTarget " \
    "receivingTouchdowns receivingYards rushingAttempts rushingAverageYards " \
    "rushingTouchdowns rushingYards kickoffReturnsTouchdowns " \
    "kickoffReturnsYards puntReturnsLong opponentFumbleRecovery " \
    "totalPointsScored kickReturnsAverageYards puntReturnsAverageYards " \
    "puntReturnsTouchdowns}id lastModifiedDate player{position jerseyNumber " \
    "currentTeam{abbreviation nickName}person{firstName lastName displayName " \
    "headshot{asset{url}}}}season{id}week{id}}}}}}&" \
    "variables=null"

LIVE_URL = "https://api.nfl.com/v3/shield/?" \
    "query=query{viewer{live{playerGameStats(gameDetailId:"{}")" \
    "{createdDate gameStats{defensiveAssists defensiveInterceptions " \
    "defensiveInterceptionsYards defensiveForcedFumble " \
    "defensivePassesDefensed defensiveSacks defensiveSafeties " \
    "defensiveSoloTackles defensiveTotalTackles defensiveTacklesForALoss " \
    "touchdownsDefense fumblesLost fumblesTotal kickReturns kickReturnsLong " \
    "kickReturnsTouchdowns kickReturnsYards kickingFgAtt kickingFgLong " \
    "kickingFgMade kickingXkAtt kickingXkMade passingAttempts " \
    "passingCompletions passingTouchdowns passingYards passingInterceptions " \
    "puntReturns puntingAverageYards puntingLong puntingPunts " \
    "puntingPuntsInside20 receivingReceptions receivingTarget " \
    "receivingTouchdowns receivingYards rushingAttempts rushingAverageYards " \
    "rushingTouchdowns rushingYards kickoffReturnsTouchdowns " \
    "kickoffReturnsYards puntReturnsLong opponentFumbleRecovery " \
    "totalPointsScored kickReturnsAverageYards puntReturnsAverageYards " \
    "puntReturnsTouchdowns}lastModifiedDate team{nickName}player{position " \
    "firstName nickName lastName}}}}}&" \
    "variables=null"

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

def load_boxscores():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
    years = soup.select("ol.year-selector a")
    for y in years:
        load_boxscores_per_year(int(y.string))

def load_boxscores_per_year(year):
    print(year)

    page = requests.get(URL + "/{}/REG1".format(year))
    soup = BeautifulSoup(page.content, "lxml")
    weeks = soup.select("a.week-item")
    print(weeks)
    for w in weeks:
        print(year)
        load_boxscores_per_week(year, w["href"].split("/")[-1])
        
def load_boxscore(year, week, id):
    print("Loading game {}...".format(id))
    page = requests.get(BOXSCORE_URL.format(id))
    soup = BeautifulSoup(page.content, "lxml")
    teams = [t.a["href"].split("=")[1] for t in
        soup.select("td.team-column-header")]
    db.session.add(models.NflBoxscoreGame(id=id, year=year, week=week,
                                          home_team=teams[1],
                                          away_team=teams[0]))
    db.session.commit()
    for (team, table) in zip(teams, soup.select("table.gc-team-leaders-table")):
        row = table.tr
        assert row["class"] == ["thd2"]
        
        # Passing
        cols = ["Passing", "CP/AT", "YDS", "TD", "INT"]
        for c, td in zip(cols, row.select("td")):
            assert td.string == c
        while True:
            row = row.find_next_sibling("tr")
            if row["class"] == ["thd2"]: break
            d = {"team": team, "game_id": id}
            cols = row.select("td")
            d["player_id"] = cols[0].a["data-id"]
            d["player_name"] = cols[0].string
            d["cp"], d["at"] = [int(x) for x in cols[1].string.split("/")]
            d["yds"] = int(cols[2].string)
            d["td"] = int(cols[3].string)
            d["int"] = int(cols[4].string)
            db.session.add(models.NflBoxscorePassing(**d))

    db.session.commit()