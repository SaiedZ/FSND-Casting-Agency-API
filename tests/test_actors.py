"""
Test suite for the actors.
"""

import json
import flaskr as flaskr

from flaskr.data.models import Actor


class TestActors:
    """Test suite for the actors."""

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

        self.actor_url = f"{self.base_url}/actors"
        self.actor_detail_url = f"{self.base_url}/actors/{self.actor_id}"

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

    def test_get_actor_without_auth_return_fails_401(self, client):
        response = client.get(self.actor_url)
        assert response.status_code == 401

    def test_create_actor_without_auth_fails_401(self, client):
        data = {"name": "james", "age": 20, "gender": "M"}
        response = client.post(self.actor_url, data=data)
        assert response.status_code == 401

    def test_update_actor_without_auth_return_status_code_401(self, client):
        data = {"name": "james", "age": 20, "gender": "M"}
        response = client.patch(self.actor_detail_url, data=data)
        assert response.status_code == 401

    def test_delete_actor_without_auth_return_fails_401(self, client):
        data = {"name": "james", "age": 20, "gender": "M"}
        response = client.delete(self.actor_detail_url, data=data)
        assert response.status_code == 401

    def test_get_actor_without_permission_fails_403(self, client, mocker):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": []})
        response = client.get(self.actor_url)
        assert response.status_code == 403

    def test_post_actor_without_permission_fails_403(self, client, mocker):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": []})
        response = client.post(self.actor_url)
        assert response.status_code == 403

    def test_delete_actor_without_permission_fails_403(
        self, client, mocker
    ):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": []})
        response = client.delete(self.actor_detail_url)
        assert response.status_code == 403

    def test_update_actor_without_permission_fails_403(
        self, client, mocker
    ):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch("flaskr.auth.auth.verify_decode_jwt",
                     return_value={"permissions": []})
        response = client.patch(self.actor_detail_url)
        assert response.status_code == 403

    def test_get_actor_with_permission_return_success(self, client, mocker):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch(
            "flaskr.auth.auth.verify_decode_jwt",
            return_value={"permissions": ["get:actors"]}
        )
        response = client.get(self.actor_url)

        assert response.status_code == 200
        assert response.json["success"] is True
        assert "actors" in response.json

    def test_post_actor_with_permission_return_success(self, client, mocker):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch(
            "flaskr.auth.auth.verify_decode_jwt",
            return_value={"permissions": ["create:actor"]},
        )

        data = {"name": "Jane", "age": 25, "gender": "F"}
        response = client.post(
            self.actor_url, data=json.dumps(data), headers=self.headers
        )

        assert response.status_code == 201
        assert response.json["success"] is True
        assert "actor" in response.json

    def test_update_actor_with_permission_success(self, client, mocker):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch(
            "flaskr.auth.auth.verify_decode_jwt",
            return_value={"permissions": ["patch:actor"]}
        )

        data = {"name": "Jannet", "gender": "F"}

        response = client.patch(
            f"{self.base_url}/actors/{self.actor.id}",
            data=json.dumps(data),
            headers=self.headers,
        )

        assert response.status_code == 200
        assert response.json["success"] is True
        assert response.json["actor"]["age"] == self.actor.age

    def test_delete_actor_with_permission_success(self, client, mocker):

        mocker.patch("flaskr.auth.auth.get_token_auth_header", return_value="")
        mocker.patch(
            "flaskr.auth.auth.verify_decode_jwt",
            return_value={"permissions": ["delete:actor"]},
        )

        response = client.delete(
            self.actor_detail_url, headers=self.headers
        )

        assert response.status_code == 200
        assert response.json["success"] is True
        assert response.json["delete"] == self.actor.id
