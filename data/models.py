"""Models
"""

import enum

from sqlalchemy.orm import validates

from .db import db


class GenderEnum(enum.Enum):

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
        if hasattr(GenderEnum, gender):
            return gender
        raise TypeError('Gender must be "M" or "F"')

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender.value,
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender.value,
            'movies': self.movies
        }

# class Genre(db.Model):

#     __tablename__ = 'genre'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)

#     movies = db.relationship(
    # 'Movie', secondary='movie_genre', backref='genres'
    # )
