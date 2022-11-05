import functools
from inspect import isclass

import pydantic
import ujson
from flask import Response, jsonify, make_response, request
from sqlalchemy.orm.query import Query

from todo.exceptions import HTTP_NOT_FOUND
from todo.orm import session


def commit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)

            if isinstance(result, tuple) and result[1] >= 300:
                session.rollback()
                return result

            session.commit()
            return result

        except Exception as ex:
            session.rollback()
            raise

    return wrapper


def json(schema, use_list=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal schema

            result = func(*args, **kwargs)

            if isinstance(result, Query):
                if use_list:
                    return Response(
                        # Using dumb loads/dumps workaround becuase pydantic doesn't
                        # support direct list serialization
                        # See https://github.com/samuelcolvin/pydantic/issues/1409
                        ujson.dumps(
                            [
                                ujson.loads(schema.from_orm(row).json(by_alias=True))
                                for row in result
                            ]
                        ),
                        mimetype='application/json',
                    )

                row = result.one_or_none()
                if row is None:
                    raise HTTP_NOT_FOUND()

                return Response(
                    schema.from_orm(row).json(by_alias=True),
                    mimetype='application/json',
                )

            elif isclass(schema) and issubclass(schema, pydantic.BaseModel):
                if not use_list:
                    if isinstance(result, dict):
                        result = schema(**result).json(by_alias=True)
                    else:
                        result = schema.from_orm(result).json(by_alias=True)
                else:
                    # Using dumb loads/dumps workaround becuase pydantic doesn't
                    # direct list serialization
                    # See https://github.com/samuelcolvin/pydantic/issues/1409
                    result = ujson.dumps(
                        [
                            ujson.loads(schema.from_orm(row).json(by_alias=True))
                            for row in result
                        ]
                    )
                return Response(
                    result,
                    mimetype='application/json',
                )

            elif isinstance(result, pydantic.BaseModel):
                return Response(result.json(by_alias=True), mimetype='application/json')

            raise Exception('Invalid return type')

        return wrapper

    return decorator
