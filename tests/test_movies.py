"""
This module contains the tests for the movies endpoints.
"""

import json
import flaskr as flaskr

from flaskr.data.models import Movie, Actor


class TestActors:
    """Test suite for movies endpoints."""

    @classmethod
    def setup_class(cls):
        cls.app = flaskr.create_app(test_config=True)
        cls.app_context = cls.app.test_request_context()
        cls.app_context.push()

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()

    def setup_method(self, method):
        self.base_url = f"/api/{flaskr.API_VERSION}"

        self.actor = Actor(name="james", age=20, gender="M")
        self.actor.insert()
        self.actor_id = self.actor.id

        self.movie = Movie(title="Die Hard", description="Action Movie",
                           genre="Action", release_date="09-12-1988")
        self.movie.insert()
        self.movie_id = self.movie.id

        self.movie_url = f"{self.base_url}/movies"
        self.movie_detail_url = f"{self.base_url}/movies/{self.movie_id}"

        self.headers = {
            "Content-Type": "application/json", "Accept": "application/json"
        }

    def teardown_method(self, method):
        """
        Clean up the database after each test.
        """
        movies = Movie.query.all()
        for movie in movies:
            movie.delete()

        actors = Actor.query.all()
        for actor in actors:
            actor.delete()

    def test_get_movie_without_auth_return_fails_401(self, client):
        response = client.get(self.movie_url)
        assert response.status_code == 401

    def test_create_movie_without_auth_fails_401(self, client):
        data = {"title": "Die Hard 5", "description": "Action Movie",
                "genre": "Action", "release_date": "09-12-1988"}
        response = client.post(self.movie_url, data=json.dumps(data))
        assert response.status_code == 401

    def test_update_movie_without_auth_return_status_code_401(self, client):
        data = {"title": "Die Hard 3", "description": "Action Movie",
                "genre": "Action", "release_date": "09-12-1988"}
        response = client.patch(self.movie_detail_url, data=json.dumps(data))
        assert response.status_code == 401

    def test_delete_movie_without_auth_return_fails_401(self, client):
        response = client.delete(self.movie_detail_url)
        assert response.status_code == 401

    def test_get_movies_with_permission_success(self, client, mocker):
        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": ["get:movie"]})

        response = client.get(self.movie_url)
        assert response.status_code == 200

    def test_create_movie_with_permission_success(self, client, mocker):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": ["create:movie"]})

        data = {"title": "Die Hard 5", "description": "Action Movie",
                "genre": "Action", "release_date": "09-12-1988"}

        response = client.post(
            self.movie_url, data=json.dumps(data), headers=self.headers
        )

        assert response.status_code == 201
        assert response.json["success"] is True
        assert response.json["movie"]["title"] == data["title"]

    def test_update_movie_with_permission_success(self, client, mocker):
        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": ["patch:movie"]})

        data = {"title": "Die Hard 6", "description": "Action Movie",
                "genre": "Action", "release_date": "09-12-1988"}

        response = client.patch(
            self.movie_detail_url, data=json.dumps(data), headers=self.headers
        )

        assert response.status_code == 200
        assert response.json["success"] is True
        assert response.json["movie"]["title"] == data["title"]

    def test_update_movie_actor_with_permission_success(self, client, mocker):
        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": ["patch:movie"]})

        data = {"actors": [f"{self.actor_id}"]}

        response = client.patch(
            self.movie_detail_url, data=json.dumps(data), headers=self.headers
        )

        assert response.status_code == 200
        assert response.json["success"] is True
        assert response.json["movie"]["actors"][0]["id"] == self.actor_id

    def test_delete_movie_with_permission_success(self, client, mocker):
        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": ["delete:movie"]})

        response = client.delete(self.movie_detail_url)
        assert response.status_code == 200
