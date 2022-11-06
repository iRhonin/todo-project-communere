import io
from datetime import datetime
from random import choice
from random import randint

import pytest
import sqlalchemy

from todo.authorization import create_access_token
from todo.config import configs
from todo.models import Developer
from todo.models import ProductManager
from todo.models import Project
from todo.models import Task
from todo.models import TaskDeveloper
from todo.models import TeamMember


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

    def _create_random_project(self, **kwargs):
        seed = randint(10**10, 10**12)

        data = dict(
            name=str(seed),
            owner_id=self._create_random_product_manager().id,
        )
        data.update(kwargs)
        project = Project(**data)
        self.session.save(project)

        return project

    def _create_random_task(self, **kwargs):
        seed = randint(10**10, 10**12)

        data = dict(
            name=str(seed),
            project_id=self._create_random_project().id,
        )
        data.update(kwargs)
        task = Task(**data)
        self.session.save(task)

        return task

    def _create_random_team_member(self, **kwargs):

        _project = self._create_random_project()
        _dev = self._create_random_developer()

        data = dict(
            project_id=_project.id,
            developer_id=_dev.id,
        )
        data.update(kwargs)
        team_member = TeamMember(**data)
        self.session.save(team_member)

        return team_member

    def _create_random_task_developer(self, **kwargs):
        _task = self._create_random_task()
        _developer = self._create_random_developer()

        data = dict(
            task_id=_task.id,
            developer_id=_developer.id,
        )
        data.update(kwargs)
        task_developer = TaskDeveloper(**data)
        self.session.save(task_developer)

        return task_developer

    def logout(self):
        del self._client.environ_base[AUTHORIZATION_HEADER_KEY]

    def login(self, user):
        with self.client.application.app_context():
            access_token = create_access_token(user)

        self._client.environ_base[AUTHORIZATION_HEADER_KEY] = access_token
        return access_token

    def login_as_pm(self):
        _user = self._create_random_product_manager()
        return self.login(_user)

    def login_as_dev(self):
        _user = self._create_random_developer()
        return self.login(_user)
