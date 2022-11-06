import os
import re
from logging import basicConfig

import psycopg2
import sqlalchemy
from flasgger import Swagger
from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pydantic.error_wrappers import ValidationError

from todo.config import configs
from todo.exceptions import HTTPException
from todo.orm import create_engine
from todo.orm import init_model
from todo.orm import session


basicConfig(level=configs.LOGLEVEL)
app = Flask(__name__)
app.config.update(configs.to_dict())
jwt = JWTManager()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  # Only for testing
Swagger(app)
jwt.init_app(app)

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(ValidationError)
def handle_pydantic_validation_errors(e):
    return jsonify(e.errors()), 400


@app.before_first_request
def init_orm():
    engine = session.bind or create_engine(url=configs.postgres_url)
    init_model(engine)


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    session.remove()
    return response_or_exc
