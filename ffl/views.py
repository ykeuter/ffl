from ffl import app, db, models, espn
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
    if not 'token' in session:
        return espn.initDraft()
        token, teams, order = espn.initDraft()
        session['token'] = token
        session['teams'] = teams
        session['order'] = order
    token = session['token']
    teams = session['teams']
    order = session['order']
    picks, index = espn.getDraft(token)
    print index
    print teams
    print order
    return teams[order[index]].teamAbbrev if index < len(order) else "FINISHED"

