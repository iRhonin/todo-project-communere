from argon2.exceptions import VerifyMismatchError
from flask import jsonify
from flask_pydantic import validate

from todo.app import api_v1
from todo.authorization import create_access_token
from todo.exceptions import HTTP_BAD_REQUEST
from todo.models import User
from todo.orm import session
from todo.schemas import LoginResultSchema, LoginSchema


@api_v1.post('/login')
@validate()
def login(body: LoginSchema):
    """
    ---
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: Login
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    definitions:
      LoginResult:
        type: object
        properties:
          accessToken:
            type: string
    responses:
      200:
        description: LoginResult
        schema:
          $ref: '#/definitions/LoginResult'
    """
    HTTP_WRONG_USER_OR_PASS = HTTP_BAD_REQUEST(message='Username or password is wrong')
    user = session.query(User).filter(User.username == body.username).one_or_none()
    if user is None:
        raise HTTP_WRONG_USER_OR_PASS

    try:
        user.validate_password(body.password)
    except VerifyMismatchError:
        raise HTTP_WRONG_USER_OR_PASS

    return dict(accessToken=create_access_token(user))
