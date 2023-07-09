from rest_framework.test import APITestCase

from tests.factories import user_factories
from tests.mocks.user_mocks import (
    user_data,
    user_expected_data,
    user_message_data
)


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/"

        colaborator_data = user_data.users_data["colaborator_data"]
        student_data = user_data.users_data["student_data"]

        cls.colaborator, cls.colaborator_token = (
            user_factories.create_colaborator_with_token(colaborator_data)
        )

        cls.student, cls.student_token = (
            user_factories.create_student_with_token(student_data)
        )

    def test_user_creation_with_invalid_data(self):
        invalid_data = user_data.invalid_data["user_data"]

        response = self.client.post(
            path=self.BASE_URL,
            data=invalid_data,
            format="json"
        )

        expected_status_code = 400
        expected_body = user_expected_data.expected_data[
            "invalid_expected"
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

    def test_colaborator_creation(self):
        colaborator_data = user_data.users_data["colaborator_two_data"]

        response = self.client.post(
            path=self.BASE_URL,
            data=colaborator_data,
            format="json"
        )

        expected_status_code = 201
        expected_body = {
            **user_expected_data.dinamic_response(response),
            "is_colaborator": True
        }

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = ("Verify if returned body for valid"
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

    def test_student_creation(self):
        student_data = user_data.users_data["student_two_data"]

        response = self.client.post(
            path=self.BASE_URL,
            data=student_data,
            format="json"
        )

        expected_status_code = 201
        expected_body = {
            **user_expected_data.dinamic_response(response),
            "is_colaborator": False,
            "status_for_loan": True
        }

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = ("Verify if returned body for valid"
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

    def test_unique_email_and_username(self):
        student_data = user_data.users_data["student_data"]

        response = self.client.post(
            path=self.BASE_URL,
            data=student_data,
            format="json"
        )

        expected_status_code = 400
        expected_body = user_expected_data.expected_data[
            "email_username_already_in_use"
        ]

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = ("Verify if returned body for non unique"
                        " email/username is correct")

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

    def test_if_non_authenticated_user_cannot_list(self):
        response = self.client.get(path=self.BASE_URL)

        expected_status_code = 401
        response_status_code = response.status_code

        message = "Verify if get method requires an authenticated token"

        self.assertEqual(expected_status_code, response_status_code, message)

    def test_if_a_student_can_list_own_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.get(path=self.BASE_URL)

        expected_status_code = 200
        expected_body = {
            **user_expected_data.dinamic_self(self),
            "is_colaborator": False,
            "status_for_loan": True
        }

        response_status_code = response.status_code
        response_body = response.json()["results"][0]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = ("Verify if returned body for list"
                        " student is correct")

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

    def test_if_a_colaborator_can_list_all_users(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.get(path=self.BASE_URL)

        expected_status_code = 200
        expected_count = 2

        response_status_code = response.status_code
        response_count = response.json()["count"]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_count = ("Verify if returned count for list"
                         " all users is correct")

        self.assertEqual(
            expected_status_code,
            response_status_code,
            message_status_code
        )
        self.assertEqual(
            expected_count,
            response_count,
            message_count
        )
