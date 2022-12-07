"""
This module contains the routes for the actors resource.
"""

from flask import Blueprint, jsonify, abort, request

from data.models import Actor
from utils import Paginator, handle_db_crud_errors
from auth.auth import requires_auth

actors_blueprint = Blueprint('actors_blueprint', __name__)


@actors_blueprint.route('/actors', methods=['GET'])
@requires_auth("get:actors")
def get_actors():
    """Gets all actors

    Returns
    -------
    JSON:
        sucess: bool
            will be True if the request was successfully handled.
        actors: list of json objects
            description of actors.
    Response code: int
        200.

    Raises
    -------
    500: server error
        if fetching actors from db fails.
    """
    try:
        actors = Actor.query.all()
    except Exception as e:
        print(e)
        abort(500)

    paginator = Paginator(items=actors, request=request)

    return jsonify({
            'success': True,
            'page': paginator.page,
            'pages': paginator.pages,
            'next_page': paginator.next_page_number or False,
            'next_page_url': paginator.next_page_url or False,
            'actors': paginator.get_next_page_items(),
            'total_actors': len(actors),
        }), 200


@actors_blueprint.route('/actors', methods=['POST'])
@requires_auth('create:actor')
def create_actor():
    """Creates a new actor.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        actor: JSON
            a formatted representation of the created actor.
    Response code: int
        201

    Notes
    -------
    See the decorator handle_db_crud_errors for more information about the
    errors that can be raised.
    """

    data = request.get_json()

    try:
        name, age, gender = data['name'], data['age'], data['gender']
    except KeyError:
        abort(400, 'Actor\'s data must contain name and age and gender')

    @handle_db_crud_errors
    def create_actor_helper():
        actor = Actor(
            name=name,
            age=age,
            gender=gender
        )
        actor.insert()
        return actor

    actor = create_actor_helper()

    return jsonify({"success": True, "actor": actor.format()}), 201


@actors_blueprint.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actor(id):
    """Updates an existing actor.

    Parameters
    -------
    id: int
        the id of the actor to be updated.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        actor: JSON
            a formatted representation of the updated actor.
    Response code: int
        200

    Notes
    -------
    See the decorator handle_db_crud_errors for more information about the
    errors that can be raised.
    """
    actor = Actor.query.get_or_404(id)

    data = request.get_json()

    if data is None:
        abort(400, 'No data was found.')

    @handle_db_crud_errors
    def update_actor_helper():
        actor.name = data.get('name') or actor.name
        actor.age = data.get('age') or actor.age
        actor.gender = data.get('gender') or actor.gender
        actor.update()
        return actor

    actor = update_actor_helper()

    return jsonify({"success": True, "actor": actor.format()}), 200


@actors_blueprint.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(id):
    """Deletes an existing actor.

    Parameters
    -------
    id: int
        the id of the actor to be deleted.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        detele: int
            the id of the deleted actor.
    Response code: int
        200

    """
    actor = Actor.query.get_or_404(id)

    try:
        actor.delete()
    except Exception as e:
        print(e)
        abort(500)

    return jsonify({"success": True, "delete": id}), 200
