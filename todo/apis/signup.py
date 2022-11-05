from flask import jsonify
from flask_pydantic import validate

from todo.app import api_v1
from todo.authorization import create_access_token
from todo.decorators import commit, json
from todo.exceptions import HTTP_BAD_REQUEST
from todo.models import Developer, ProductManager, User
from todo.orm import safe_commit, session
from todo.schemas import SignupResultSchema, UserDto, UserSchema


@api_v1.post('/signup/developer')
@validate()
@json(SignupResultSchema)
@commit
def signup_developer(body: UserDto):
    """
    ---
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: Signup-Developer
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    definitions:
      Signup:
        type: object
        properties:
          user:
            $ref: '#/definitions/User'
          tokens:
            $ref: '#/definitions/LoginResult'
      User:
        type: object
        properties:
          id:
            type: integer
          username:
            type: string
          type:
            type: string
    responses:
      200:
        schema:
          $ref: '#/definitions/Signup'
    """
    return _signup(model=Developer, data=body)


@api_v1.post('/signup/product-manager')
@validate()
@json(SignupResultSchema)
@commit
def signup_pm(body: UserDto):
    """
    ---
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: Signup-Product-Manager
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        schema:
          $ref: '#/definitions/Signup'
    """
    return _signup(model=ProductManager, data=body)


def _signup(model, data):
    username_exists = session.query(
        session.query(User).filter(User.username == data.username).exists()
    ).scalar()

    if username_exists:
        raise HTTP_BAD_REQUEST(message='Username already exists')

    user = model(username=data.username, password=data.password)
    session.add(user)
    safe_commit(session)

    user_dict = UserSchema.from_orm(user)
    access_token = create_access_token(user)
    return dict(user=user_dict, tokens=dict(access_token=access_token))
