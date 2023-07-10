from rest_framework.test import APITestCase

from copies.models import Copy
from tests.factories import user_factories, book_factories, follow_factories
from tests.mocks.user_mocks import (
    user_data,
    user_expected_data,
    user_message_data,
)
from tests.mocks.follower_mocks import follow_expected_data
from tests.mocks.book_mocks import book_data


class FollowViewTest(APITestCase):
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

        cls.follow = follow_factories.create_follower(
            cls.book_two,
            cls.student,
        )

        cls.BASE_URL = "/api/follow/"

    def test_if_a_non_logged_user_cant_follow_a_book(self):
        base_url = self.BASE_URL + str(self.book.id) + "/"
        response = self.client.post(
            path=base_url,
            student=self.student,
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

    def test_if_a_colaborator_cant_follow_a_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.colaborator_token
        )
        base_url = self.BASE_URL + str(self.book.id) + "/"
        response = self.client.post(
            path=base_url,
            student=self.student,
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

    def test_if_a_student_can_follow_a_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        base_url = self.BASE_URL + str(self.book.id) + "/"
        response = self.client.post(
            path=base_url,
            student=self.student,
        )

        expected_status_code = 201
        expected_body = follow_expected_data.dinamic_self(
            self.follow.id + 1,
            self.student,
            self.book
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

    def test_if_a_student_cant_follow_a_book_twice(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        base_url = self.BASE_URL + str(self.book_two.id) + "/"
        response = self.client.post(
            path=base_url,
            student=self.student,
        )

        expected_status_code = 409
        expected_body = {
            "detail": "You already follow this book"
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
