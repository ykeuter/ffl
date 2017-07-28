from ffl import app, db, models
from flask import render_template, session, flash, redirect, url_for, request

@app.route('/')
def show_players():
    players = models.NflPlayer.query.all()
    return render_template('show_players.html', players=players)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('show_players'))

@app.route('/logout')
def logout():
    return redirect(url_for('show_players'))

