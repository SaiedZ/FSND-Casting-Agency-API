from flask import Blueprint, jsonify, abort, request

from data.models import Movie

movies_blueprint = Blueprint('movies_blueprint', __name__)
