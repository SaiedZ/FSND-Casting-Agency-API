"""
This module contains the routes for a simple healthcheck.
"""

from flask import Blueprint, jsonify, abort

from ..data.models import Actor, Movie


health_blueprint = Blueprint('health_blueprint', __name__)


@health_blueprint.route('/health', methods=['GET'])
def get_health():
    """Gets health of the app

    Returns
    -------
    JSON:
        sucess: bool
            will be True if the request was successfully handled.
        actors: int
            number of actors.
        movies: int
            number of movies.
    Response code: int
        200.

    Raises
    -------
    500: server error
        if fetching actors from db fails.
    """
    try:
        actors = Actor.query.all()
        movies = Movie.query.all()
    except Exception as e:
        print(e)
        abort(500)

    return jsonify({
            'success': True,
            'actors': len(actors),
            'movies': len(movies)
        }), 200
