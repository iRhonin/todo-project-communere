from tests.helper import LOGIN_URL, BaseTestClass


class TestLogin(BaseTestClass):
    def mockup(self):
        self.password = '123456'
        self.developer = self._create_random_developer(password=self.password)
        self.pm = self._create_random_product_manager(password=self.password)

    def test_login_as_developer(self):
        res = self.client.post(
            LOGIN_URL,
            json={
                'username': self.developer.username,
                'password': self.password,
            },
        )
        self.assert_ok(res)
        assert res.json['accessToken'] is not None

        res = self.client.post(
            LOGIN_URL,
            json={
                'username': self.developer.username,
                'password': 'invalid-pass',
            },
        )
        self.assert_code(res, 400)

        res = self.client.post(
            LOGIN_URL,
            json={
                'username': 'invalid-username',
                'password': self.password,
            },
        )
        self.assert_code(res, 400)

    def test_login_as_pm(self):
        res = self.client.post(
            LOGIN_URL,
            json={
                'username': self.pm.username,
                'password': self.password,
            },
        )
        self.assert_ok(res)
        assert res.json['accessToken'] is not None
