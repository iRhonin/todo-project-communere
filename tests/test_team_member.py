from tests.helper import BaseTestClass


PROJECT_TEAM_MEMBERS_URL = '/api/v1/team-members'


class TestTeamMember(BaseTestClass):
    def mockup(self):
        self.pm1 = self._create_random_product_manager()
        self.project1 = self._create_random_project(owner_id=self.pm1.id)
        self.developer1 = self._create_random_developer()

    def test_add_team_member(self):
        self.login(self.pm1)

        res = self.client.post(
            PROJECT_TEAM_MEMBERS_URL,
            json={
                'developerId': self.developer1.id,
                'projectId': self.project1.id,
            },
        )
        self.assert_ok(res)

    def test_add_team_member_as_not_owner(self):
        self.login_as_pm()

        res = self.client.post(
            PROJECT_TEAM_MEMBERS_URL,
            json={
                'developerId': self.developer1.id,
                'projectId': self.project1.id,
            },
        )
        self.assert_code(res, 403)

    def test_add_team_member_unathorized(self):
        res = self.client.post(
            PROJECT_TEAM_MEMBERS_URL,
            json={
                'developerId': self.developer1.id,
                'projectId': self.project1.id,
            },
        )
        self.assert_code(res, 401)

    def test_add_team_member_twice(self):
        self.login(self.pm1)
        res = self.client.post(
            PROJECT_TEAM_MEMBERS_URL,
            json={
                'developerId': self.developer1.id,
                'projectId': self.project1.id,
            },
        )
        res = self.client.post(
            PROJECT_TEAM_MEMBERS_URL,
            json={
                'developerId': self.developer1.id,
                'projectId': self.project1.id,
            },
        )
        self.assert_code(res, 400)

    def test_add_team_member_developer_not_found(self):
        self.login(self.pm1)
        res = self.client.post(
            PROJECT_TEAM_MEMBERS_URL,
            json={
                'developerId': -1,
                'projectId': self.project1.id,
            },
        )
        self.assert_code(res, 400)

    def test_add_team_member_project_not_found(self):
        self.login(self.pm1)
        res = self.client.post(
            PROJECT_TEAM_MEMBERS_URL,
            json={
                'developerId': self.developer1.id,
                'projectId': -1,
            },
        )
        self.assert_code(res, 400)
