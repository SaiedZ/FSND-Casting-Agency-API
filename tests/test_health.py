"""
Test suite for the health check.
"""

from string import ascii_lowercase
import flaskr as flaskr

from flaskr.data.models import Actor, Movie


class TestHealth:
    """Test suite for the health check."""

    @classmethod
    def setup_class(cls):
        cls.app = flaskr.create_app(test_config=True)
        cls.app_context = cls.app.test_request_context()
        cls.app_context.push()

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()

    def setup_method(self, method):

        self.url = f"/api/{flaskr.API_VERSION}/health"

        for i in range(1, 11):
            movie = Movie(
                title=f"movie{i}", release_date="01-01-2020", genre="Action"
            )
            movie.insert()
            actor = Actor(
                name=f"actor{ascii_lowercase[i]}", gender="F", age=20
            )
            actor.insert()

        self.headers = {
            "Content-Type": "application/json", "Accept": "application/json"
        }

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

    def test_get_health_success(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json["success"] is True
        assert "actors" in response.json
        assert response.json["actors"] == 10
        assert "movies" in response.json
        assert response.json["movies"] == 10
