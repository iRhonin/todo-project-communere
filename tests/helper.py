import io
from datetime import datetime
from random import choice, randint

import pytest
import sqlalchemy

from todo.authorization import create_access_token
from todo.config import configs
from todo.models import Developer, ProductManager

LOGIN_URL = '/api/v1/login'
AUTHORIZATION_HEADER_KEY = 'HTTP_AUTHORIZATION'


class BaseTestClass:
    _authorization__ = None

    @pytest.fixture(scope='function', autouse=True)
    def init_class(self, db, client):
        configs.TESTING = True

        # DBSession
        self.session = db()

        # Insert mockup data
        self.mockup()

        # # Disable Sentry
        # import sentry_sdk

        # sentry_sdk.init()

        # get client
        self._client = client

    @property
    def client(self):
        return self._client

    def mockup(self):
        # Override this method to add mockup data
        pass

    @classmethod
    def assert_code(cls, res, code):
        assert res.status_code == code, res.json

    @classmethod
    def assert_ok(cls, res):
        cls.assert_code(res, 200)

    def _create_random_developer(self, **kwargs):
        seed = randint(10**10, 10**12)
        while True:
            try:
                data = dict(
                    username=seed,
                    password='password',
                )
                data.update(kwargs)
                user = Developer(**data)
                self.session.save(user)
                break
            except sqlalchemy.exc.IntegrityError:
                continue

        return user

    def _create_random_product_manager(self, **kwargs):
        seed = randint(10**10, 10**12)
        while True:
            try:
                data = dict(
                    username=seed,
                    password='password',
                )
                data.update(kwargs)
                user = ProductManager(**data)
                self.session.save(user)
                break
            except sqlalchemy.exc.IntegrityError:
                continue

        return user

    def logout(self):
        del self._client.environ_base[AUTHORIZATION_HEADER_KEY]

    def login(self, user=None):
        _user = user or self._create_random_user()

        with self.client.application.app_context():
            access_token = create_access_token(_user)

        self._client.environ_base[AUTHORIZATION_HEADER_KEY] = access_token
        return access_token
