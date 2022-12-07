"""Auth0 authorization and authentication flow."""

import os
import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ALGORITHMS = os.getenv("ALGORITHMS")
API_AUDIENCE = os.getenv("API_AUDIENCE")


class AuthError(Exception):
    """AuthError Exception
    A standardized way to communicate auth failure modes.
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header

    Returns:
    ------
    The token part of the header.

    Raises
    -------
    AuthError if:
        no header is present
        the header is malformed

    """

    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    """Checks in user have the requested permission.

    Parameters:
    ------
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    Returns:
    ------
    True

    Raises
    -------
    AuthError if:
        permissions are not included in the payload
        the requested permission string is not in the payload permissions
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


# NOTE urlopen has a common certificate error described here:
# https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org


def verify_decode_jwt(token, auth0_domain, algorithms, audience):
    """Verrifies if a token is valid.

    Parameters:
    ------
        token: a json web token (string)

    Returns:
    ------
        the decoded payload
    Raises
    -------
    AuthError if:
        token is not valid.
    """

    jsonurl = urlopen(f'https://{auth0_domain}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=algorithms,
                audience=audience,
                issuer='https://' + auth0_domain + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': ('Incorrect claims. Please, '
                                'check the audience and issuer.')
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    """Verrify if the user have the required permissions

    Parameters:
    ------
        permission: string permission (i.e. 'post:drink')

    Returns:
    ------
        the decorator which passes the decoded payload to the decorated method
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token,
                                            auth0_domain=AUTH0_DOMAIN,
                                            algorithms=ALGORITHMS,
                                            audience=API_AUDIENCE)
                check_permissions(permission, payload)
            except AuthError as e:
                abort(e.status_code, e.error)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
