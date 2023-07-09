from rest_framework.test import APITestCase

from tests.factories import user_factories, book_factories
from tests.mocks.user_mocks import (
    user_data,
    user_expected_data,
    user_message_data
)
from tests.mocks.book_mocks import book_data, book_expected_data


class BookDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
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
        cls.book_two = book_factories.create_book(
            book_data.book_data["sql"],
            colaborator=cls.colaborator
        )

        cls.BASE_URL = f"/api/books/{cls.book.id}/"

    def test_if_non_authenticated_user_cant_list_books(self):
        response = self.client.get(path=self.BASE_URL)

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

    def test_if_an_authenticated_user_can_list_a_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.get(path=self.BASE_URL)

        expected_status_code = 200
        expected_body = book_expected_data.dinamic_self(self.book)

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
