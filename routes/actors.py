from flask import Blueprint, jsonify, abort, request
from sqlalchemy import exc

from data.models import Actor

actors_blueprint = Blueprint('actors_blueprint', __name__)


@actors_blueprint.route('/actors', methods=['GET'])
def get_actors():
    try:
        actors = Actor.query.all()
    except Exception as e:
        print(e)
        abort(500)

    return jsonify({
            'success': True,
            'actors': [actor.short() for actor in actors]
        }), 200


@actors_blueprint.route('/actors/<int:id>', methods=['GET'])
def get_actor_detail(id):

    actor = Actor.query.get_or_404(id)

    return jsonify({
            'success': True,
            'actors': actor.long()
        }), 200


@actors_blueprint.route('/actors', methods=['POST'])
def create_actor():

    data = request.get_json()

    try:
        name, age, gender = data['name'], data['age'], data['gender']
    except ValueError:
        abort(400, 'Actor\'s data must contain name and age and gender')

    try:
        actor = Actor(
            name=name,
            age=age,
            gender=gender
        )
        actor.insert()

    except TypeError as e:
        print(e)
        abort(400, f"ERROR: {e}")

    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        print(e)
        abort(400, f"ERROR: {err_msg}")

    except Exception as e:
        print(e)
        abort(500)

    return jsonify({"success": True, "actor": [actor.short()]})
