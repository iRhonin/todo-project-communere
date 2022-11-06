import os
from logging import DEBUG as DEBUG_LVL

from dotenv import find_dotenv
from dotenv import load_dotenv


class Config(object):
    ENVIRONMENT = 'local'
    DEBUG = True
    LOGLEVEL = DEBUG_LVL
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = '5432'
    POSTGRES_DB = 'todo'
    POSTGRES_TEST_DB = 'todo_test'
    POSTGRES_ADMIN_DB = 'postgres'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'postgres'
    JWT_SECRET_KEY = 'axcasdxaobisduba'
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 3600  # 1 day
    JWT_REFRESH_TOKEN_EXPIRES = 3 * 30 * 24 * 3600  # 3 months
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SWAGGER = {
        "specs": [
            {
                "openapi": "3.0.3",
                "version": "1.0",
                "title": "Todo Apis",
                "endpoint": "api",
                "route": "/api/v1",
            }
        ]
    }

    def __init__(self):
        load_dotenv(find_dotenv())

        for k, v in os.environ.items():
            if not k.startswith('TODO_'):
                continue
            key = k.replace('TODO_', '')
            v = self._cast(v)

            setattr(self, key, v)

    def _cast(self, v):
        try:
            v = float(v)
            if v.is_integer():
                v = int(v)
        except ValueError:
            if v == 'false':
                v = False
            elif v == 'true':
                v = True
            elif v == 'null' or v == 'None':
                v = None
            else:
                pass

        return v

    @property
    def postgres_url(self):
        return (
            f'postgresql://'
            f'{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )

    @property
    def postgres_test_url(self):
        return (
            f'postgresql://'
            f'{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_TEST_DB}'
        )

    @property
    def postgres_admin_url(self):
        return (
            f'postgresql://'
            f'{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_ADMIN_DB}'
        )

    def to_dict(self):
        return dict(
            (key, getattr(self, key))
            for key in dir(self)
            if not key.startswith('__') and not callable(getattr(self, key))
        )


configs: Config = Config()
