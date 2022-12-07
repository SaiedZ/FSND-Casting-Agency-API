"""Module to handle errors when creating, updating or deleting"""

from functools import wraps

from flask import abort
from sqlalchemy import exc


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
