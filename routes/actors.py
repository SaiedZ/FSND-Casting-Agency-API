"""
This module contains the routes for the actors resource.
"""

from functools import wraps

from flask import Blueprint, jsonify, abort, request
from sqlalchemy import exc

from data.models import Actor
from utils.paginator import Paginator

actors_blueprint = Blueprint('actors_blueprint', __name__)


def handle_db_crud_errors(func):
    """Decorator to handle errors when creating, updating or deleting

    Parameters
    -------
    func: function
        the function to be decorated

    Returns
    -------
    result:
        the result returned by the decorated function: func

    Raises
    -------
    400: TypeError
        if model's attributes sent by the user doesn't match the expected types
    400: IntegrityError
        if the action could not be performed due to a database integrity error
    500: server error
        the error's message is returned in the response body
    """

    @wraps(func)
    def wrapped_func(*args, **kwargs):

        try:
            result = func()

        except TypeError as e:
            print(e)
            abort(400, f"ERROR: {e}")

        except exc.IntegrityError as e:
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            print(e)
            abort(400, f"ERROR: {err_msg}")

        except Exception as e:
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            print(e)
            abort(500, f"ERROR: {err_msg}")

        return result

    return wrapped_func


@actors_blueprint.route('/actors', methods=['GET'])
def get_actors():
    """Gets all actors

    Returns
    -------
    JSON:
        sucess: bool
            will be True if the request was successfully handled.
        actors: list of json objects
            short description of actors.
    Response code: int
        200.

    Raises
    -------
    500: server error
        if fetching actors failed.
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
    except ValueError:
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

    return jsonify({"success": True, "actor": [actor.format()]}), 201


@actors_blueprint.route('/actors/<int:id>', methods=['PATCH'])
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

    return jsonify({"success": True, "actor": [actor.format()]})


@actors_blueprint.route('/actors/<int:id>', methods=['DELETE'])
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
