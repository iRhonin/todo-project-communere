from tests.helper import BaseTestClass


LIST_PROJECT_TASKS_URL = '/api/v1/projects/%s/tasks'


class TestListTask(BaseTestClass):
    def mockup(self):
        self.pm1 = self._create_random_product_manager()
        self.dev1 = self._create_random_developer()
        self.dev2 = self._create_random_developer()
        self.project1 = self._create_random_project(owner_id=self.pm1.id)
        self.project2 = self._create_random_project(owner_id=self.pm1.id)
        self.task1 = self._create_random_task(project_id=self.project1.id)
        self.task2 = self._create_random_task(project_id=self.project1.id)
        self.task3 = self._create_random_task(project_id=self.project1.id)

    def test_list_project_task_as_pm(self):
        self.login(self.pm1)

        res = self.client.get(
            LIST_PROJECT_TASKS_URL % self.project1.id,
        )
        self.assert_ok(res)
        assert len(res.json) == 3

    def test_list_project_task_as_dev(self):
        self.login(self.dev1)
        self._create_random_team_member(
            developer_id=self.dev1.id,
            project_id=self.project1.id,
        )

        res = self.client.get(
            LIST_PROJECT_TASKS_URL % self.project1.id,
        )
        self.assert_ok(res)
        assert len(res.json) == 3

    def test_list_project_task_as_non_team_member_dev(self):
        self.login(self.dev1)
        res = self.client.get(
            LIST_PROJECT_TASKS_URL % self.project1.id,
        )
        self.assert_code(res, 403)

    def test_list_project_task_filter_by_user(self):
        self.login(self.pm1)
        self._create_random_task_developer(
            developer_id=self.dev2.id,
            task_id=self.task3.id,
        )
        self._create_random_task_developer(
            developer_id=self.dev2.id,
            task_id=self.task2.id,
        )

        res = self.client.get(
            LIST_PROJECT_TASKS_URL % self.project1.id,
            query_string=dict(
                developerId=self.dev2.id,
            ),
        )
        self.assert_ok(res)
        assert len(res.json) == 2

        res = self.client.get(
            LIST_PROJECT_TASKS_URL % self.project1.id,
            query_string=dict(
                developerId=self.dev1.id,
            ),
        )
        self.assert_ok(res)
        assert len(res.json) == 0
