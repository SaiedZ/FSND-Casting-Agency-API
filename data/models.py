"""Models
"""

import enum
from .db import db


class GenderEnum(enum.Enum):

    MALE = "M"
    FEMALE = "F"


movie_actor = db.Table(
    "association", db.Model.metadata,
    db.Column(
        "movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column(
        "actor_id", db.Integer, db.ForeignKey("actor.id"), primary_key=True),
)


class Movie(db.Model):

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String)

    actors = db.relationship(
        "Actor", secondary=movie_actor,
        backref=db.backref('movies', lazy=True),
        cascade="save-update"
    )

    def __repr__(self):
        return f"<Movie id: {self.id} - title: {self.title}>"

    def __str__(self):
        return self.title


class Actor(db.Model):

    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)

    def __repr__(self):
        return f"<Actor id: {self.id} - name: {self.name}>"

    def __str__(self):
        return self.name


# class Genre(db.Model):

#     __tablename__ = 'genre'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)

#     movies = db.relationship(
    # 'Movie', secondary='movie_genre', backref='genres'
    # )
