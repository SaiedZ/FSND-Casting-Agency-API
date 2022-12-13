"""
Module to handel the SQLAlchemy database creation and migration process
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def db_setup(app):
    """setup the database for the app.

    Returns:
    --------
    db:
        the database instance
    """

    db.init_app(app)
    Migrate(app, db)
    return db
