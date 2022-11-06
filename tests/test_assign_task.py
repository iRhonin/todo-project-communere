from tests.helper import BaseTestClass


ASSIGN_TASK_URL = '/api/v1/tasks/%s/assign'


class TestAssignTask(BaseTestClass):
    def mockup(self):
        self.pm1 = self._create_random_product_manager()
        self.dev1 = self._create_random_developer()
        self.project1 = self._create_random_project(owner_id=self.pm1.id)
        self.task1 = self._create_random_task(project_id=self.project1.id)

    def test_assign_task_as_pm(self):
        self.login(self.pm1)

        res = self.client.post(
            ASSIGN_TASK_URL % self.task1.id,
            json={
                'developerId': self.dev1.id,
            },
        )
        self.assert_ok(res)
        assert res.json['developers'][0]['id'] == self.dev1.id

    def test_add_task_as_developer(self):
        self.login(self.dev1)
        self._create_random_team_member(
            developer_id=self.dev1.id,
            project_id=self.project1.id,
        )
        res = self.client.post(
            ASSIGN_TASK_URL % self.task1.id,
            json={
                'developerId': self.dev1.id,
            },
        )
        self.assert_ok(res)
        assert res.json['developers'][0]['id'] == self.dev1.id

    def test_assign_task_twice(self):
        self.login(self.pm1)

        res = self.client.post(
            ASSIGN_TASK_URL % self.task1.id,
            json={
                'developerId': self.dev1.id,
            },
        )
        res = self.client.post(
            ASSIGN_TASK_URL % self.task1.id,
            json={
                'developerId': self.dev1.id,
            },
        )
        self.assert_code(res, 400)

    def test_add_task_as_unathorized(self):
        res = self.client.post(
            ASSIGN_TASK_URL % self.task1.id,
            json={
                'developerId': self.dev1.id,
            },
        )
        self.assert_code(res, 401)

    def test_add_task_as_non_team_member_dev(self):
        self.login_as_dev()
        res = self.client.post(
            ASSIGN_TASK_URL % self.task1.id,
            json={
                'developerId': self.dev1.id,
            },
        )
        self.assert_code(res, 403)

    def test_add_task_as_non_owner_pm(self):
        self.login_as_pm()
        res = self.client.post(
            ASSIGN_TASK_URL % self.task1.id,
            json={
                'developerId': self.dev1.id,
            },
        )
        self.assert_code(res, 403)
