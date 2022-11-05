import os
from logging import DEBUG as DEBUG_LVL

from dotenv import find_dotenv, load_dotenv


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
    API_URL = 'http://0.0.0.0:5000'
    REDIS_HOST = 'redis'
    REDIS_PORT = '6379'
    JWT_SECRET_KEY = 'axcasdxaobisduba'
    JSON_SORT_KEYS = False
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 3600  # 1 day
    JWT_REFRESH_TOKEN_EXPIRES = 3 * 30 * 24 * 3600  # 3 months
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SWAGGER = {
        "specs": [
            {
                "version": "2.0",
                "title": "Todo Apis",
                "endpoint": "api",
                "route": "/api/v1",
            }
        ]
    }

    def __init__(self):
        load_dotenv(find_dotenv())

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

    @property
    def redis_url(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    def to_dict(self):
        return dict(
            (key, getattr(self, key))
            for key in dir(self)
            if not key.startswith('__') and not callable(getattr(self, key))
        )


configs: Config = Config()
