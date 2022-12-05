import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import ProductionConfig, DevelopmentConfig, TestingConfig

from data.models import Movie, Actor
from data.db import db_setup


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)

    if os.environ.get('IS_DEPLOYED', False):
        app.config.from_object(ProductionConfig)
    elif test_config is not None:
        app.config.from_object(test_config)
    else:
        app.config.from_object(DevelopmentConfig)

    CORS(app)
    db = db_setup(app)

    with app.app_context():
        db.create_all()

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080)
