from rest_framework.test import APITestCase

from tests.factories import user_factories
from tests.mocks.user_mocks import user_data, user_expected_data, user_message_data


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/login"

        colaborator_data = user_data.users_data["colaborator_data"]
        student_data = user_data.users_data["student_data"]

        cls.colaborator, cls.colaborator_token = (
            user_factories.create_colaborator_with_token(colaborator_data)
        )

        cls.student, cls.student_token = (
            user_factories.create_student_with_token(student_data)
        )

        cls.maxDiff = None

    def test_login_without_body_data(self):
        response = self.client.post(path=self.BASE_URL)

        expected_status_code = 400
        expected_body = user_expected_data.expected_data[
            "username_password_fileds_required"
        ]

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = ("Verify if returned body for empty"
                        " data is correct")

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
        expected_body = user_expected_data.expected_data[
            "no_active_account_found"
        ]

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = ("Verify if returned body for invalid"
                        " data is correct")

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

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = ("Verify if returned body for valid"
                        " data is refresh and access token")

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
