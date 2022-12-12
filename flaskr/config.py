from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    # Grabs the folder where the script runs.
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    TESTING = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(Config.BASEDIR, 'data', 'prod_db.sqlite3')}"
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(Config.BASEDIR, 'data', 'dev_db.sqlite3')}"
    )


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(Config.BASEDIR, 'data', 'test_db.sqlite3')}"
    )
