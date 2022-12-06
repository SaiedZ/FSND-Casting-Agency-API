"""Module to """

from flask import jsonify, Blueprint

error_handlers_blueprint = Blueprint('error_handlers_blueprint', __name__)


@error_handlers_blueprint.app_errorhandler(400)
def bad_request(error):
    message = error.description or "Bad request"
    return (
        jsonify(
            {"success": False,
                "error": 400,
                "message": message}
        ),
        400
    )


@error_handlers_blueprint.app_errorhandler(401)
def unauthorized(error):
    message = error.description or "Unauthorized"
    return (
        jsonify(
            {"success": False,
                "error": 401,
                "message": message}
        ),
        401
    )


@error_handlers_blueprint.app_errorhandler(404)
def not_found(error):
    message = error.description or "Not found"
    return (
        jsonify(
            {"success": False,
                "error": 404,
                "message": message}
        ),
        404,
    )


@error_handlers_blueprint.app_errorhandler(422)
def unprocessable(error):
    message = error.description or "Unprocessable"
    return jsonify({
        "success": False,
        "error": 422,
        "message": message
    }), 422


@error_handlers_blueprint.app_errorhandler(500)
def internal_server_error(error):
    message = error.description or "Internal Server Error"
    return (
        jsonify(
            {"success": False,
                "error": 500,
                "message": message}
        ),
        500
    )
