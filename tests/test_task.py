from tests.helper import BaseTestClass


TASKS_URL = '/api/v1/tasks'


class TestTask(BaseTestClass):
    def mockup(self):
        self.pm1 = self._create_random_product_manager()
        self.dev1 = self._create_random_developer()
        self.project1 = self._create_random_project(owner_id=self.pm1.id)

    def test_add_task_as_pm(self):
        self.login(self.pm1)

        res = self.client.post(
            TASKS_URL,
            json={
                'name': 'task1',
                'projectId': self.project1.id,
            },
        )
        self.assert_ok(res)
        assert res.json['id'] is not None
        assert res.json['name'] is not None
        assert res.json['projectId'] == self.project1.id
        assert res.json['developers'] == []

    def test_add_task_as_developer(self):
        self.login(self.dev1)
        self._create_random_team_member(
            developer_id=self.dev1.id,
            project_id=self.project1.id,
        )
        res = self.client.post(
            TASKS_URL,
            json={
                'name': 'task1',
                'projectId': self.project1.id,
            },
        )
        self.assert_ok(res)
        assert res.json['id'] is not None
        assert res.json['name'] is not None
        assert res.json['projectId'] == self.project1.id
        assert res.json['developers'][0]['id'] == self.dev1.id

    def test_add_task_as_unathorized(self):
        res = self.client.post(
            TASKS_URL,
            json={
                'name': 'task1',
                'projectId': self.project1.id,
            },
        )
        self.assert_code(res, 401)

    def test_add_task_as_non_team_member_dev(self):
        self.login_as_dev()
        res = self.client.post(
            TASKS_URL,
            json={
                'name': 'task1',
                'projectId': self.project1.id,
            },
        )
        self.assert_code(res, 403)

    def test_add_task_as_non_owner_pm(self):
        self.login_as_pm()
        res = self.client.post(
            TASKS_URL,
            json={
                'name': 'task1',
                'projectId': self.project1.id,
            },
        )
        self.assert_code(res, 403)
