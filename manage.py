from ffl import app, db, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import csv

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def load_schedule():
    with open('data/schedule.csv') as f:
        r = csv.reader(f)
        teams = []
        r.next()
        teams = [{"name": row[0], "bye_week": row.index("BYE") - 1}
                    for row in r]
    db.session.bulk_insert_mappings(models.Team, teams)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
