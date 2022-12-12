"""
This is the main module of the application.

It contains the app factory, applies config, sets the database and the CORS.s
"""

import os

from flask import Flask
from flask_cors import CORS

from .config import ProductionConfig, DevelopmentConfig, TestingConfig

from .data.models import Movie, Actor  # noqa
from .data.db import db_setup

from .utils import error_handlers_blueprint
from .routes import actors_blueprint, movies_blueprint
from .routes import oauth_blueprint, oauth


API_VERSION = "v1"


def create_app(test_config=False):
    """Creates and configure the app

    params:
        test_config:boolean - if set to True, the TestingConfig will be applied
    returns:
        the flask app
    """

    # Creating the Flask app
    app = Flask(__name__)

    # Applying the config
    if os.environ.get("IS_DEPLOYED", False):
        app.config.from_object(ProductionConfig)

    elif test_config:
        app.config.from_object(TestingConfig)

    else:
        app.config.from_object(DevelopmentConfig)

    # Setting Cors
    CORS(app)

    # Register blueprints
    app.register_blueprint(
        error_handlers_blueprint, url_prefix=f"/api/{API_VERSION}")

    app.register_blueprint(
        actors_blueprint, url_prefix=f"/api/{API_VERSION}")

    app.register_blueprint(
        movies_blueprint, url_prefix=f"/api/{API_VERSION}")

    app.register_blueprint(oauth_blueprint)

    # Setting up the database
    db = db_setup(app)

    with app.app_context():
        db.create_all()

    # Setting up the Auth0
    oauth.init_app(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
