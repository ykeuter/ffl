from ffl import app, db, models, espn, nfl, shark
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import csv

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def delete_data():
    db.session.execute(models.playerPosition.delete())
    models.EspnProjections.query.delete()
    models.SharkProjections.query.delete()
    models.NflPlayer.query.delete()
    models.Position.query.delete()
    models.NflGame.query.delete()
    models.FieldTeam.query.delete()
    models.FieldPlayer.query.delete()
    db.session.commit()
    print("Deleted all data.")

@manager.command
def shark_proj(period=app.config['SHARK_SEGMENT'],
               scoring=app.config['SHARK_SCORING']):
    shark.update_projections(int(period), int(scoring))

@manager.command
def shark_check():
    shark.check_sanity()

@manager.command
def espn_proj(league_id=app.config['ESPN_LEAGUE_ID']):
    espn.update_projections(int(league_id))

@manager.command
def update_boxscores(year=None, week=None):
    if year is None:
        models.NflGame.query.delete()
        db.session.commit()
        nfl.load_boxscores()
    elif week is None:
        models.NflGame.query.filter_by(season_value=int(year)).delete()
        db.session.commit()
        nfl.load_boxscores_per_year(int(year))
    else:
        models.NflGame.query.filter_by(
                season_value=int(year), week_order=int(week)).delete()
        db.session.commit()
        nfl.load_boxscores_per_year(int(year), int(week))

@manager.command
def update_players():
    dummy = models.FieldPlayer(espn_id=-1,
                               shark_id=-1,
                               name="dummy")
    db.session.add(dummy)
    players = models.FieldPlayer.query.all()
    with open(app.config['PLAYERS_FILE']) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            sh = next((p for p in players if p.shark_id == int(row[1])),
                      None)
            es = next((p for p in players if p.espn_id == int(row[0])),
                      None)
            if sh:
                if sh is es:
                    continue
                dummy.shark_projections = sh.shark_projections
                db.session.delete(sh)
            if es:
                dummy.espn_projections = es.espn_projections
                db.session.delete(es)
            db.session.commit()
            p = models.FieldPlayer(espn_id=int(row[0]),
                                   shark_id=int(row[1]),
                                   name=row[2],
                                   shark_projections=dummy.shark_projections,
                                   espn_projections=dummy.espn_projections)
            db.session.add(p)
            db.session.commit()
    db.session.delete(dummy)
    db.session.commit()

@manager.command
def load_data():
    delete_data()

    with open(app.config['PLAYERS_FILE']) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            db.session.add(models.FieldPlayer(espn_id=int(row[0]),
                                              shark_id=int(row[1]),
                                              name=row[2]))
        db.session.commit()

    with open(app.config['TEAMS_FILE']) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            db.session.add(models.FieldTeam(espn_id=int(row[2]),
                                            espn_code=row[1],
                                            name=row[0],
                                            shark_code=row[3]))
        db.session.commit()

    # BYE_STRING = "BYE"
    # with open(app.config['SCHEDULE_FILE']) as f:
    #     r = csv.reader(f)
    #     r.next()
    #     for row in r:
    #         home = next(x for x in teams if x.espn_code == row[0])
    #         home.bye_week = row.index(BYE_STRING)
    #         for i in xrange(1, len(row)):
    #             away = next((x for x in teams if x.espn_code == row[i]), None)
    #             if away != None: db.session.add(models.NflGame(home, away, i))
    # db.session.commit()

    with open(app.config['POSITIONS_FILE']) as f:
        r = csv.reader(f)
        next(r)
        positions = [models.Position(espn_code=row[0],
            name=row[1], order=row[2]) for row in r]
        for p in positions:
            db.session.add(p)
    db.session.commit()

#    DEF_STRING = "D"
#    FA_STRING = "FA"
#    with open(app.config['PROJECTIONS_FILE']) as f:
#        r = csv.reader(f)
#        r.next()
#        for row in r:
#            if len(row) == 0:
#                break
#            if row[2] == FA_STRING:
#                t = None
#            else:
#                t = next((x for x in teams if x.fs_name == row[2]), None)
#            if row[3] == DEF_STRING:
#                t.projected_defense_points = row[14]
#            else:
#                db.session.add(models.NflPlayer(row[1], t, [x for x in positions if x.code ==
#                    row[3]], row[14]))
#    db.session.commit()

    print("Loaded all reference data.")

if __name__ == '__main__':
    manager.run()
