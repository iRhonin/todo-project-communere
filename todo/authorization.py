import functools
from logging import getLogger

from flask import jsonify, make_response
from flask.globals import request
from flask_jwt_extended import create_access_token as _create_access_token
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError

from todo.app import jwt
from todo.config import configs
from todo.exceptions import HTTP_PERMISION_DENIED, HTTP_UNAUTHORIZED
from todo.models import Developer, ProductManager
from todo.orm import session
from todo.roles import *

BEARER = 'Bearer '
ROLE_KEY = 'role'


def get_user_role():
    verify_jwt_in_request()
    return get_jwt_claims().get(ROLE_KEY)


def create_access_token(user, fresh=False):
    return BEARER + _create_access_token(
        identity=user.id,
        fresh=fresh,
        additional_claims={
            'username': user.username,
            ROLE_KEY: user.type,
        },
    )


def authorize(*roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_id = get_jwt_identity()
                user_role = claims.get(ROLE_KEY, USER)

                if user_role not in roles:
                    raise HTTP_PERMISION_DENIED()

                user = None
                if user_role == Roles.DEVELOPER:
                    user = (
                        session.query(Developer)
                        .filter(Developer.id == user_id)
                        .one_or_none()
                    )
                elif user_role == Roles.PRODUCT_MANAGER:
                    user = (
                        session.query(ProductManager)
                        .filter(
                            ProductManager.id == user_id,
                        )
                        .one_or_none()
                    )
                else:
                    raise HTTP_UNAUTHORIZED()

                if user is None:
                    raise HTTP_UNAUTHORIZED()

                request.user = user

            except (PyJWTError, JWTExtendedException) as ex:
                raise HTTP_UNAUTHORIZED()

            return func(*args, **kwargs)

        return wrapper

    return decorator


# Note: do not remove verify function, if u do, get_jwt_identity will return None!
def get_user_id():
    verify_jwt_in_request()
    return get_jwt_identity()
