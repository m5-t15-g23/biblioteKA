from rest_framework.test import APITestCase

from tests.mocks.user_mocks import (
    user_data,
    user_expected_data,
    user_message_data
)
from tests.factories import (
    copy_factories,
    user_factories,
    book_factories,
    loan_factories
)
from tests.mocks.book_mocks import book_data
from tests.mocks.loan_mocks import loan_data, loan_expected_data


class LoanViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        colaborator_data = user_data.users_data["colaborator_data"]
        student_data = user_data.users_data["student_data"]
        student_two_data = user_data.users_data["student_two_data"]

        cls.colaborator, cls.colaborator_token = (
            user_factories.create_colaborator_with_token(colaborator_data)
        )
        cls.student, cls.student_token = (
            user_factories.create_student_with_token(student_data)
        )
        cls.student_two, cls.student_two_token = (
            user_factories.create_student_with_token(student_two_data)
        )

        cls.book = book_factories.create_book(
            book_data.book_data["clean_code"],
            colaborator=cls.colaborator
        )
        cls.book_two = book_factories.create_book(
            book_data.book_data["sql"],
            colaborator=cls.colaborator
        )

        copy_one, copy_two, copy_three = (
            copy_factories.create_copies(cls.book)
        )
        cls.copies = [copy_one, copy_two, copy_three]

        cls.copy_one, cls.copy_two, cls.copy_three = (
            copy_factories.create_copies(cls.book_two)
        )

        cls.loan = loan_factories.create_loan(
            cls.student,
            cls.copy_one
        )

        cls.BASE_URL = f"/api/loans/"

    def test_if_non_authenticated_user_cant_create_loans(self):
        base_url = self.BASE_URL + str(self.book.id) + "/"

        response = self.client.post(
            path=base_url,
        )

        expected_status_code = 401
        expected_body = user_expected_data.expected_data[
            "credentials_not_provided"
        ]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "credentials_not_provided"
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

    def test_if_an_colaborator_cant_create_an_loan(self):
        base_url = self.BASE_URL + str(self.book.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.post(
            path=base_url,
        )

        expected_status_code = 403
        expected_body = user_expected_data.expected_data[
            "non_permission"
        ]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "student_authorization"
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

    def test_create_loan_with_non_existing_book(self):
        base_url = self.BASE_URL + "9999/"
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.post(path=base_url)

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

    def test_if_a_student_can_create_an_loan(self):
        base_url = self.BASE_URL + str(self.book.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.post(
            path=base_url,
        )

        expected_status_code = 201
        expected_body = loan_expected_data.dinamic_response(
            loan_data.loan_data["new_loan"],
            self.student,
            self.copy_one.id,
            self.book.title,
            self.loan.id + 1
        )

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

    def test_if_a_student_cant_have_more_than_3_loans(self):
        base_url = self.BASE_URL + str(self.book.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_two_token
        )
        for _ in self.copies:
            self.client.post(path=base_url)

        response = self.client.post(
            path=base_url,
        )

        expected_status_code = 409
        expected_body = {
            "detail": "User alredy blocked"
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

    def test_if_a_student_cant_loan_an_not_available_book(self):
        base_url = self.BASE_URL + str(self.book.id) + "/"

        for _ in self.copies:
            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + self.student_two_token
            )
            self.client.post(path=base_url)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.post(
            path=base_url,
        )

        expected_status_code = 409
        expected_body = {
            "detail": ("This book is not available, follow to check"
                       "availability status.")
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
