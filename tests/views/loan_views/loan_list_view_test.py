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


class LoanListViewTest(APITestCase):
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
        cls.loan_two = loan_factories.create_loan(
            cls.student_two,
            cls.copy_two
        )

        cls.BASE_URL = "/api/loans/"

    def test_if_non_authenticated_user_cant_list_loans(self):
        response = self.client.get(
            path=self.BASE_URL,
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

    def test_if_an_colaborator_can_list_all_loans(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.get(
            path=self.BASE_URL,
        )

        expected_status_code = 200
        expected_body = [
            loan_expected_data.dinamic_self(
                self.loan,
                self.student,
                self.copy_one.id,
                self.book.title
            ),
            loan_expected_data.dinamic_self(
                self.loan_two,
                self.student_two,
                self.copy_two.id,
                self.book.title
            )
        ]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_body = user_message_data.message_data[
            "message_body_is_correct"
        ]

        response_status_code = response.status_code
        response_body = response.json()["results"]

        self.assertEqual(
            expected_status_code,
            response_status_code,
            message_status_code
        )
        self.assertListEqual(
            expected_body,
            response_body,
            message_body
        )
