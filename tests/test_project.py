from tests.helper import BaseTestClass


PROJECT_URL = '/api/v1/projects'
PROJECT_TEAM_MEMBERS_URL = '/api/v1/projects/%s/team-members'


class TestProject(BaseTestClass):
    def test_add_project(self):
        self.login_as_pm()
        res = self.client.post(
            PROJECT_URL,
            json={
                'name': 'project1',
            },
        )
        self.assert_ok(res)
        assert res.json['id'] is not None
        assert res.json['owner'] is not None

    def test_add_project_as_unathorized(self):
        res = self.client.post(
            PROJECT_URL,
            json={
                'name': 'project1',
            },
        )
        self.assert_code(res, 401)

    def test_add_project_as_developer(self):
        self.login_as_dev()
        res = self.client.post(
            PROJECT_URL,
            json={
                'name': 'project1',
            },
        )
        self.assert_code(res, 403)

    def test_list_project(self):
        pm1 = self._create_random_product_manager()
        self.login(pm1)
        self._create_random_project(owner_id=pm1.id)

        res = self.client.get(
            PROJECT_URL,
        )
        self.assert_ok(res)
        assert len(res.json) == 1
