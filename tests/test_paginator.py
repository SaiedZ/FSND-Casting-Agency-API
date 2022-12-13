"""
Test suite for the Paginator
"""

from string import ascii_lowercase

import flaskr as flaskr
from flaskr.utils import Paginator
from flaskr.constants import ITEM_PER_PAGE
from flaskr.data.models import Actor, Movie


class RequestMock(object):
    """Mock class for the request object."""

    class ArgsMock:
        """Mock class for the request.args object."""

        def __init__(self, args):
            self.args = args

        def get(self, key, default, type):
            """Mock the get method of the request.args object."""
            return self.args.get(key, default)

    def __init__(self, args, base_url):
        self.args = self.ArgsMock(args)
        self.base_url = base_url


class TestPaginator:
    """Test suite for the Paginator."""

    @classmethod
    def setup_class(cls):
        cls.app = flaskr.create_app(test_config=True)
        cls.app_context = cls.app.test_request_context()
        cls.app_context.push()

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()

    def setup_method(self, method):

        self.request = RequestMock(args={"page": 3}, base_url="local/")

        for i in range(1, 11):
            movie = Movie(
                title=f"movie{i}", release_date="01-01-2020", genre="Action"
            )
            movie.insert()
            actor = Actor(
                name=f"actor{ascii_lowercase[i]}", gender="F", age=20
            )
            actor.insert()

    def teardown_method(self, method):
        """
        Clean up the database after each test.
        """
        actors = Actor.query.all()
        for actor in actors:
            actor.delete()
        movies = Movie.query.all()
        for movie in movies:
            movie.delete()

    def test_paginate_actors_success(self, client):
        """Test the pagination of actors."""
        actors = Actor.query.all()
        paginator = Paginator(actors, self.request)
        actors = paginator.get_next_page_items()
        assert len(actors) == ITEM_PER_PAGE
        assert paginator.next_page_number
        assert paginator.next_page_url

    def test_paginate_moviess_success(self, client):
        """Test the pagination of movies."""
        movies = Movie.query.all()
        paginator = Paginator(movies, self.request)
        movies = paginator.get_next_page_items()
        assert len(movies) == ITEM_PER_PAGE
        assert paginator.next_page_number
        assert paginator.next_page_url
