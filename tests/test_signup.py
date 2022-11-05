from tests.helper import BaseTestClass

SIGNUP_DEVELOPER_URL = '/api/v1/signup/developer'
SIGNUP_PM_URL = '/api/v1/signup/product-manager'


class TestSignup(BaseTestClass):
    def test_signup_as_developer(self):
        res = self.client.post(
            SIGNUP_DEVELOPER_URL,
            json={
                'username': 'test-dev',
                'password': '123456',
            },
        )
        self.assert_ok(res)
        assert res.json['tokens']['accessToken'] is not None
        assert res.json['user']['id'] is not None
        assert res.json['user']['type'] is not None
        assert res.json['user']['username'] is not None
        assert res.json['user']['createdAt'] is not None
        assert 'password' not in res.json['user']

    def test_signup_as_pm(self):
        res = self.client.post(
            SIGNUP_PM_URL,
            json={
                'username': 'test-pm',
                'password': '123456',
            },
        )
        self.assert_ok(res)
        assert res.json['tokens']['accessToken'] is not None
        assert res.json['user']['id'] is not None
        assert res.json['user']['type'] is not None
        assert res.json['user']['username'] is not None
        assert 'password' not in res.json['user']

    def test_signup_dupplicate_username(self):
        self._create_random_developer(username='abcd')
        res = self.client.post(
            SIGNUP_PM_URL,
            json={
                'username': 'abcd',
                'password': '123456',
            },
        )
        self.assert_code(res, 400)
