"""Models
"""

import enum
from datetime import datetime

from sqlalchemy.orm import validates

from .db import db
from utils.movie_genre import MovieGenreEnum


class GenderEnum(enum.Enum):
    """Utility class to Actor, used for gender attribute"""

    M = "Male"
    F = "Female"


class ModelCrudDbHelper():

    def insert(self):
        """inserts a new model into a database

        EXAMPLE: a_givern_model.insert()
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a model into a database

        The model must exist in the database
        EXAMPLE: a_givern_model.update()
        """
        db.session.commit()

    def delete(self):
        """Deletes a new model into a database

        The model must exist in the database
        EXAMPLE: a_givern_model.delete()
        """
        db.session.delete(self)
        db.session.commit()


movie_actor = db.Table(
    "association", db.Model.metadata,
    db.Column(
        "movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column(
        "actor_id", db.Integer, db.ForeignKey("actor.id"), primary_key=True),
)


class Movie(db.Model, ModelCrudDbHelper):

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    genre = db.Column(db.Enum(MovieGenreEnum), nullable=True)
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

    @validates('title')
    def validates_title(self, key, title):
        """Validates the title attribute

        Should contain at least 5 characters
        """
        if len(title) < 5:
            raise TypeError('Title must contain at least 5 characters')
        return title

    @validates('release_date')
    def validates_release_date(self, key, release_date):
        """Validates the release_date attribute.

        Should be in the format DD-MM-YYYY.
        """
        try:
            datetime.strptime(release_date, '%d-%m-%Y')
        except ValueError as e:
            raise ValueError(
                "Incorrect data format, should be DD-MM-YYYY"
            ) from e
        return datetime.strptime(release_date, '%d-%m-%Y')

    @validates('genre')
    def validates_genre(self, key, genre):
        """validates the genre attribute.

        See MovieGenreEnum class.
        """
        if hasattr(MovieGenreEnum, genre):
            return genre
        raise TypeError(
            'Genre must be one of the following: '
            f'{", ".join([genre.value for genre in MovieGenreEnum])}'
        )

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'genre': self.genre.value,
            'description': self.description,
            'actors': [actor.short_format() for actor in self.actors],
            'num_actors': len(self.actors),
        }

    def short_format(self):
        """
        Short format used for serialization of moviesin actor's format method
        """
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'genre': self.genre.value,
            'description': self.description,
        }


class Actor(db.Model, ModelCrudDbHelper):

    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)

    def __repr__(self):
        return f"<Actor id: {self.id} - name: {self.name}>"

    def __str__(self):
        return self.name

    @validates('name')
    def validate_name(self, key, name):
        """Validates the name attribute.

        Should contain only alphabetic characters and at least 3 characters.
        """
        if not name.isalpha():
            raise TypeError('Name must containonly alphabetic characters')
        if len(name) < 3:
            raise TypeError('Name must contain at least 3 characters')
        return name

    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int):
            raise TypeError('Age must be an integer')
        if age < 0:
            raise TypeError('Age must be greater than 0')
        return age

    @validates('gender')
    def validate_gender(self, key, gender):
        """Validates the gender attribute.

        See GEnderEnum class.
        """
        if hasattr(GenderEnum, gender):
            return gender
        raise TypeError('Gender must be "M" or "F"')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender.value,
            'movies': [movie.short_format() for movie in self.movies],
            'number_movies': len(self.movies),
        }

    def short_format(self):
        """
        Short description of the actor used in movie's format method.
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender.value,
        }
