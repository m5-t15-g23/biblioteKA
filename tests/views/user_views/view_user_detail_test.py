from rest_framework.test import APITestCase
from datetime import datetime as dt, timedelta as td

from tests.factories import user_factories, book_factories, copy_factories
from tests.mocks.user_mocks import (
    user_data,
    user_expected_data,
    user_message_data
)
from tests.mocks.book_mocks import book_data

from loans.models import Loan


class UserDetailViewTest(APITestCase):
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

        cls.book = book_factories.create_book(
            book_data.book_data["clean_code"],
            colaborator=cls.colaborator
        )

        cls.copy_one, cls.copy_two, cls.copy_three = (
            copy_factories.create_copies(cls.book)
        )

    def test_list_student_status_without_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"
        response = self.client.get(path=base_url)

        expected_status_code = 401
        response_status_code = response.status_code

        message = user_message_data.message_data[
            "non_give_authentication_class"
        ]

        self.assertEqual(expected_status_code, response_status_code, message)

    def test_list_student_status_with_student_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.get(path=base_url)

        expected_status_code = 403
        expected_body = user_expected_data.expected_data[
            "non_permission"
        ]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "colaborator_authorization"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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

    def test_list_non_existing_student(self):
        base_url = self.BASE_URL + "9999/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.get(path=base_url)

        expected_status_code = 404
        expected_body = user_expected_data.expected_data[
            "not found"
        ]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "message_body_is_correct"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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

    def test_list_student_status_with_colaborator_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.get(path=base_url)

        expected_status_code = 200
        expected_body = {
            "id": self.student.id,
            "email": self.student.email,
            "username": self.student.username,
            "status_for_loan": True
        }

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "message_body_is_correct"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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

    def test_patch_student_status_without_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"
        response = self.client.patch(path=base_url)

        expected_status_code = 401
        response_status_code = response.status_code

        message = user_message_data.message_data[
            "non_give_authentication_class"
        ]

        self.assertEqual(expected_status_code, response_status_code, message)

    def test_patch_student_status_with_student_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.patch(path=base_url)

        expected_status_code = 403
        expected_body = user_expected_data.expected_data[
            "non_permission"
        ]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "colaborator_authorization"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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

    def test_patch_non_existing_student(self):
        base_url = self.BASE_URL + "9999/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.patch(path=base_url)

        expected_status_code = 404
        expected_body = user_expected_data.expected_data[
            "not found"
        ]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "message_body_is_correct"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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

    def test_patch_student_with_zero_loans_status(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.patch(path=base_url)

        expected_status_code = 406
        expected_body = {
            "detail": "User didn't have loans yet"
        }

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "message_body_is_correct"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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

    def test_patch_student_with_loan_in_permited_period_status(self):
        student = self.student
        copy = self.copy_one
        loan_return = dt.now() + td(days=1)
        Loan.objects.create(user=student, copy=copy, loan_return=loan_return)

        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.patch(path=base_url)

        expected_status_code = 406
        expected_body = {
            "detail": "User first loan is already in permited period"
        }

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "message_body_is_correct"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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

    def test_patch_student_with_loan_in_ultrapssed_period_status(self):
        student = self.student
        copy = self.copy_one
        loan_return = dt.now() - td(days=1)
        Loan.objects.create(user=student, copy=copy, loan_return=loan_return)

        data = {
            "status_for_loan": False
        }

        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.patch(path=base_url, data=data, format="json")

        expected_status_code = 200
        expected_body = {
            **user_expected_data.dinamic_self(self.student),
            "is_colaborator": False,
            "status_for_loan": False
        }

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "message_body_is_correct"
        ]

        response_status_code = response.status_code
        response_body = response.json()

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
