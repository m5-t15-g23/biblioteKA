from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.models import User


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/login"

        cls.colaborator = User.objects.create_superuser(
            email="colaborator@mail.com",
            username="colaborator",
            password="1234",
            first_name="colabo",
            last_name="rator",
            is_colaborator=True
        )

        cls.colaborator_access_token = str(
            AccessToken.for_user(cls.colaborator)
        )
        cls.colaborator_refresh_token = str(
            RefreshToken.for_user(cls.colaborator)
        )

        cls.maxDiff = None

    def test_login_without_body_data(self):
        response = self.client.post(path=self.BASE_URL)

        expected_status_code = 400
        expected_body = {
            "username": [
                "This field is required."
            ],
            "password": [
                "This field is required."
            ]
        }

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = (f"Verify if returned status_code for invalid"
                               f" data is {expected_status_code}")
        message_body = (f"Verify if returned body for empty"
                        f" data is correct")

        self.assertEqual(
            expected_status_code,
            response_status_code,
            message_status_code
        )
        self.assertDictEqual(
            expected_body,
            response_body,
            message_body
        )

    def test_login_with_invalid_credentials(self):
        data = {
            "username": "random",
            "password": "random"
        }

        response = self.client.post(path=self.BASE_URL, data=data)

        expected_status_code = 401
        expected_body = {
            "detail": "No active account found with the given credentials"
        }

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = (f"Verify if returned status_code for invalid"
                               f" data is {expected_status_code}")
        message_body = (f"Verify if returned body for invalid"
                        f" data is correct")

        self.assertEqual(
            expected_status_code,
            response_status_code,
            message_status_code
        )
        self.assertDictEqual(
            expected_body,
            response_body,
            message_body
        )

    def test_login_with_valid_user_data(self):
        data = {
            "username": "colaborator",
            "password": "1234"
        }

        response = self.client.post(path=self.BASE_URL, data=data)

        expected_status_code = 200
        expected_keys = {"refresh", "access"}

        response_status_code = response.status_code
        response_keys = set(response.json().keys())

        message_status_code = (f"Verify if returned status_code for invalid"
                               f" data is {expected_status_code}")
        message_body = (f"Verify if returned body for valid"
                        f" data is refresh and access token")

        self.assertEqual(
            expected_status_code,
            response_status_code,
            message_status_code
        )
        self.assertSetEqual(
            expected_keys,
            response_keys,
            message_body
        )
