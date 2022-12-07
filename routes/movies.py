"""
This module contains the routes for the movies resource.
"""

from flask import Blueprint, jsonify, abort, request

from data.models import Movie, Actor
from utils import Paginator, handle_db_crud_errors
from auth.auth import requires_auth

movies_blueprint = Blueprint('movies_blueprint', __name__)


@movies_blueprint.route('/movies', methods=['GET'])
@requires_auth('get:movie')
def get_movies():
    """Gets all movies

    Returns
    -------
    JSON:
        sucess: bool
            will be True if the request was successfully handled.
        movies: list of json objects
            description of movies.
    Response code: int
        200.

    Raises
    -------
    500: server error
        if fetching movies from db fails.
    """
    try:
        movies = Movie.query.all()
    except Exception as e:
        print(e)
        abort(500)

    paginator = Paginator(items=movies, request=request)

    return jsonify({
        'success': True,
        'page': paginator.page,
        'pages': paginator.pages,
        'next_page': paginator.next_page_number or False,
        'next_page_url': paginator.next_page_url or False,
        'movies': paginator.get_next_page_items(),
        'total_movies': len(movies),
    }), 200


@movies_blueprint.route('/movies', methods=['POST'])
@requires_auth('create:movie')
def create_movie():
    """Creates a new movie.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        movie: JSON
            description of the created movie.
    Response code: int
        201.

    Notes
    -------
    See the decorator handle_db_crud_errors for more information about the
    errors that can be raised.
    """

    data = request.get_json()

    movie_dict = {}

    try:
        movie_dict['title'] = data['title']
        movie_dict['release_date'] = data['release_date']
    except KeyError:
        abort(400, 'Movie\'s data must contain a title and release_date')

    if 'genre' in data:
        movie_dict['genre'] = data['genre']
    if 'description' in data:
        movie_dict['description'] = data['description']
    if 'actors' in data:
        actors = _get_actors_from_list_of_actors_id(data['actors'])
        movie_dict['actors'] = actors

    @handle_db_crud_errors
    def create_movie_helper():
        movie = Movie(**movie_dict)
        movie.insert()
        return movie

    movie = create_movie_helper()

    return jsonify({"success": True, "movie": movie.format()}), 201


@movies_blueprint.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movie(id):
    """Updates a movie.

    Parameters
    -------
    id: int
        id of the movie to update.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        movie: JSON
            description of the updated movie.
    Response code: int
        200.

    Notes
    -------
    See the decorator handle_db_crud_errors for more information about the
    errors that can be raised.
    """
    movie = Movie.query.get_or_404(id)

    data = request.get_json()

    if data is None:
        abort(400, 'No data provided')

    @handle_db_crud_errors
    def update_movie_helper():

        movie.title = data.get('title') or movie.title
        movie.release_date = data.get('release_date') or movie.release_date
        movie.genre = data.get('genre') or movie.genre
        movie.description = data.get('description') or movie.description
        if 'actors' in data:
            actors = _get_actors_from_list_of_actors_id(data['actors'])
            movie.actors = actors

        movie.update()

        return movie

    movie = update_movie_helper()

    return jsonify({"success": True, "movie": movie.format()}), 200


@movies_blueprint.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(id):
    """Deletes a movie.

    Parameters
    -------
    id: int
        id of the movie to delete.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
    Response code: int
        200.

    Notes
    -------
    See the decorator handle_db_crud_errors for more information about the
    errors that can be raised.
    """
    movie = Movie.query.get_or_404(id)

    @handle_db_crud_errors
    def delete_movie_helper():
        movie.delete()

    delete_movie_helper()

    return jsonify({"success": True, "delete": id}), 200


def _get_actors_from_list_of_actors_id(actors_id: list[int]) -> list[Actor]:
    """Gets a list of actors from a list of actors ids.

    Parameters
    -------
    actors_id: list of int
        list of actors ids.

    Returns
    -------
    list of Actor:
        list of actors fetched from the database.

    Raises
    -------
    400: 'actors must be a list of actor ids'
    400: 'Invalid actor id, should be int'
    """
    actors = []

    if not isinstance(actors_id, list):
        abort(400, 'actors must be a list of actor ids')
    try:
        actors_id = {int(actor_id) for actor_id in actors_id}
    except ValueError:
        abort(400, 'Invalid actor id, should be int')

    for actor_id in actors_id:
        actor = Actor.query.get_or_404(actor_id)
        actors.append(actor)

    return actors
