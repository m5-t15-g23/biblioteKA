from rest_framework.test import APITestCase

from copies.models import Copy
from tests.factories import user_factories, book_factories
from tests.mocks.user_mocks import (
    user_data,
    user_expected_data,
    user_message_data
)
from tests.mocks.book_mocks import book_data, book_expected_data


class BookViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/books/"

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

    def test_if_a_non_logged_user_cant_create_a_book(self):
        data = book_data.book_data["clean_code"]

        response = self.client.post(
            path=self.BASE_URL,
            data=data,
            format="json"
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

    def test_if_a_student_cant_create_a_book(self):
        data = book_data.book_data["clean_code"]

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.post(
            path=self.BASE_URL,
            data=data,
            format="json"
        )

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

    def test_book_cration_with_invalid_data(self):
        data = book_data.invalid_data[
            "invalid_book"
        ]

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.post(
            path=self.BASE_URL,
            data=data,
            format="json"
        )

        expected_status_code = 400
        expected_body = book_expected_data.expected_data[
            "invalid_expected"
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

    def test_if_a_colaborator_can_create_a_book(self):
        data = book_data.book_data["sql"]

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        response = self.client.post(
            path=self.BASE_URL,
            data=data,
            format="json"
        )

        expected_status_code = 201
        expected_body = book_expected_data.dinamic_response(
            data,
            self.book_two.id + 1
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

    def test_if_copies_are_created_with_a_book_creation(self):
        data = book_data.book_data["sql"]

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        self.client.post(
            path=self.BASE_URL,
            data=data,
            format="json"
        )

        copies = Copy.objects.all()
        copies_number = data["copies_number"]

        message = ("Verify if book view are creating copies and make sure"
                   " that the number of copies is equal to copies_number"
                   " field in book input")

        self.assertTrue(
            len(copies) == copies_number,
            message
        )

    def test_list_all_books(self):
        response = self.client.get(path=self.BASE_URL)

        expected_status_code = 200
        expected_count = 2

        response_status_code = response.status_code
        response_count = response.json()["count"]

        message_status_code = user_message_data.message_status_code(
            expected_status_code
        )
        message_count = ("Verify if returned count for list"
                         " all books is correct")

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
