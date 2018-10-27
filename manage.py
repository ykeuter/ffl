from ffl import app, db, models, espn, nfl
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import csv

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def delete_data():
    db.session.execute(models.playerPosition.delete())
    models.NflPlayer.query.delete()
    models.Position.query.delete()
    models.NflGame.query.delete()
    models.NflTeam.query.delete()
    db.session.commit()
    print("Deleted all data.")

@manager.command
def update_projections():
    espn.update_projections()

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
def load_data():
    with open(app.config['TEAMS_FILE']) as f:
        r = csv.reader(f)
        next(r)
        teams = [models.NflTeam(int(row[2]), row[1], row[0]) for row in r]
    for t in teams:
        db.session.add(t)
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
