"""
This module contains the routes for the frontend routes.
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from flask import Blueprint
from flask import render_template, session, url_for, redirect

from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=(
        f'https://{env.get("AUTH0_DOMAIN")}/'
        '.well-known/openid-configuration'
    ),
)

oauth_blueprint = Blueprint('oauth_blueprint', __name__)


@oauth_blueprint.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("oauth_blueprint.callback", _external=True)
    )


@oauth_blueprint.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@oauth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("oauth_blueprint.home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@oauth_blueprint.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )
