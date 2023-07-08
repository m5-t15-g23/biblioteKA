from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/"

        cls.colaborator = User.objects.create_superuser(
            email="colaborator@mail.com",
            username="colaborator",
            password="1234",
            first_name="colabo",
            last_name="rator",
            is_colaborator=True
        )

        cls.student = User.objects.create_user(
            email="student@mail.com",
            username="student",
            password="1234",
            first_name="stu",
            last_name="dent"
        )

        cls.colaborator_token = str(AccessToken.for_user(cls.colaborator))
        cls.student_token = str(AccessToken.for_user(cls.student))

    def test_user_creation_with_invalid_data(self):
        user_data = {
            "email": "nonemail",
            "username": 1234,
            "last_name": [],
            "is_colaborator": {}
        }

        response = self.client.post(
            path=self.BASE_URL,
            data=user_data,
            format="json"
        )

        expected_status_code = 400
        expected_body = {
            "email": [
                "Enter a valid email address."
            ],
            "first_name": [
                "This field is required."
            ],
            "last_name": [
                "Not a valid string."
            ],
            "password": [
                "This field is required."
            ],
            "is_colaborator": [
                "Must be a valid boolean."
            ]
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

    def test_colaborator_creation(self):
        colaborator_data = {
            "email": "colaboratortest@mail.com",
            "username": "colaboratortest",
            "password": "1234",
            "first_name": "colabo",
            "last_name": "rator",
            "is_colaborator": True
        }

        response = self.client.post(
            path=self.BASE_URL,
            data=colaborator_data,
            format="json"
        )

        expected_status_code = 201
        expected_body = {
            "id": response.json()["id"],
            "email": response.json()["email"],
            "username": response.json()["username"],
            "first_name": response.json()["first_name"],
            "last_name": response.json()["last_name"],
            "is_colaborator": True
        }

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = (f"Verify if returned status_code for valid"
                               f" data is {expected_status_code}")
        message_body = (f"Verify if returned body for valid"
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

    def test_student_creation(self):
        student_data = {
            "email": "studenttest@mail.com",
            "username": "studenttest",
            "password": "1234",
            "first_name": "stu",
            "last_name": "dent"
        }

        response = self.client.post(
            path=self.BASE_URL,
            data=student_data,
            format="json"
        )

        expected_status_code = 201
        expected_body = {
            "id": response.json()["id"],
            "email": response.json()["email"],
            "username": response.json()["username"],
            "first_name": response.json()["first_name"],
            "last_name": response.json()["last_name"],
            "is_colaborator": False,
            "status_for_loan": True
        }

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = (f"Verify if returned status_code for valid"
                               f" data is {expected_status_code}")
        message_body = (f"Verify if returned body for valid"
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

    def test_unique_email_and_username(self):
        student_data = {
            "email": "student@mail.com",
            "username": "student",
            "password": "1234",
            "first_name": "stu",
            "last_name": "dent"
        }

        response = self.client.post(
            path=self.BASE_URL,
            data=student_data,
            format="json"
        )

        expected_status_code = 400
        expected_body = {
            "email": [
                "Email already in use"
            ],
            "username": [
                "Username already in use"
            ]
        }

        response_status_code = response.status_code
        response_body = response.json()

        message_status_code = (f"Verify if returned status_code for non unique"
                               f" email/username is {expected_status_code}")
        message_body = (f"Verify if returned body for non unique"
                        f" email/username is correct")

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
            "id": self.student.id,
            "email": self.student.email,
            "username": self.student.username,
            "first_name": self.student.first_name,
            "last_name": self.student.last_name,
            "is_colaborator": False,
            "status_for_loan": True
        }

        response_status_code = response.status_code
        response_body = response.json()["results"][0]

        message_status_code = (f"Verify if returned status_code for valid"
                               f" data is {expected_status_code}")
        message_body = (f"Verify if returned body for list"
                        f" student is correct")

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

        message_status_code = (f"Verify if returned status_code for valid"
                               f" data is {expected_status_code}")
        message_count = (f"Verify if returned count for list"
                         f" all users is correct")

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
