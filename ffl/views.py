from ffl import app, db, models, espn, draft, mcts
from flask import render_template, session, flash, redirect, url_for, request

@app.route('/team/<team_code>')
def showPlayersByTeam(team_code):
    teams = models.NflTeam.query.order_by(models.NflTeam.name).all()
    positions = models.Position.query.order_by(models.Position.order).all()

    team = next(t for t in teams if t.espn_code == team_code)

    players = models.NflPlayer.query.\
            filter(models.NflPlayer.team == team).\
            order_by(models.NflPlayer.projected_points.desc())
    players = map(lambda pos: (pos.name, url_for('showPlayersByPosition',
        pos_code=pos.espn_code), [p for p in players if pos in
        p.positions]), positions)

    return render_template('show_players.html', players=players,
            teams=teams, positions=positions,
            breadcrumbs=['Teams', team.name])

@app.route('/position/<pos_code>')
def showPlayersByPosition(pos_code):
    teams = models.NflTeam.query.order_by(models.NflTeam.name).all()
    positions = models.Position.query.order_by(models.Position.order).all()

    position = next(p for p in positions if p.espn_code == pos_code)

    players = models.NflPlayer.query.\
            filter(models.NflPlayer.positions.contains(position)).\
            order_by(models.NflPlayer.projected_points.desc())
    players = map(lambda t: (t.name, url_for('showPlayersByTeam',
        team_code=t.espn_code), [p for p in players if p.team is t]), teams)

    return render_template('show_players.html', players=players,
            teams=teams, positions=positions,
            breadcrumbs=['Positions', position.name])

@app.route('/')
def index():
    teams = models.NflTeam.query.order_by(models.NflTeam.name).all()
    positions = models.Position.query.order_by(models.Position.order).all()
    return render_template('index.html', teams=teams, positions=positions)

@app.route('/email', methods=["POST"])
def addEmail():
    e = models.UserEmail(email=request.form['email'])
    db.session.add(e)
    db.session.commit()
    flash('Your email address ' + request.form['email'] +
      ' was successfully added to our mailing list.')
    return redirect(url_for('index'))

@app.route('/draft')
def showDraft():
    NONE_STRING = "--"
    ITERMAX = 200

    nflteams = models.NflTeam.query.order_by(models.NflTeam.name).all()
    positions = models.Position.query.order_by(models.Position.order).all()

    if not 'draftToken' in session:
        token, teams, order = espn.initDraft()
        session['draftToken'] = token
        session['draftTeams'] = teams
        session['draftOrder'] = order
    token = session['draftToken']
    teams = session['draftTeams']
    order = session['draftOrder']

    picks, index = espn.getDraft(token)
    fa = draft.getFreeAgents()
    latestPick = next(p.name for p in fa if p.espn_id == picks[-1]['playerId']) \
            if picks else NONE_STRING
    nextTeam = teams[order[index]]["teamAbbrev"] \
            if index < len(order) else NONE_STRING

    rosters = [[] for _ in teams]
    turns = order[index:]
    state = draft.GameState(rosters, turns, fa)
    for pick in picks:
        player = next(p for p in fa if p.espn_id == pick['playerId'])
        state.PickFreeAgent(pick['teamId'], player)

    if request.args.get('analyze'):
        _, nodes = mcts.UCT(state, ITERMAX)
        rankings = [(n.move, "[S/V: " + "{:.2f}".format(n.score / n.visits) + " | V: " +
            str(n.visits) + "]") for n in nodes]
    else:
        rankings = [(m, None) for m in state.GetMoves()]

    return render_template('draft.html', latestPick=latestPick,
            nextTeam=nextTeam, freeagents=fa, rankings=rankings, teams=nflteams,
            positions=positions)

