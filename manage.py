from flask.ext.script import (
    Server,
    Shell,
    Manager,
)
from flask.ext.migrate import Migrate, MigrateCommand

from app.factory import create_app
from app.database import db


def _make_context():
    return dict(
        app=create_app(),
        db=db
    )


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)

manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
