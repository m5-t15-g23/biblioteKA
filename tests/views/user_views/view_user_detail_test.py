from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime as dt, timedelta as td

from users.models import User
from books.models import Book
from copies.models import Copy
from loans.models import Loan


class UserDetailViewTest(APITestCase):
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

        cls.book = Book.objects.create(
            title="Clean Code",
            author="Robert C. Martin",
            description="How to write clean code",
            page_numbers=500,
            language="English",
            genre="Education",
            copies_number=3
        )

        cls.book_copies = [Copy.objects.create(book=cls.book)
                           for _ in range(3)]
        cls.copies = Copy.objects.all()
        cls.copy_one = cls.copies[0]
        cls.copy_two = cls.copies[1]
        cls.copy_three = cls.copies[2]

    def test_list_student_status_without_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"
        response = self.client.get(path=base_url)

        expected_status_code = 401
        response_status_code = response.status_code

        message = "Verify authentication class was given"

        self.assertEqual(expected_status_code, response_status_code, message)

    def test_list_student_status_with_student_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.get(path=base_url)

        expected_status_code = 403
        expected_body = {
            "detail": "You do not have permission to perform this action."
        }

        message_status_code = "Verify if return status code is 403"
        message_body = "Verify if permission class only auhtorize colaborators"

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
            "id": 2,
            "email": "student@mail.com",
            "username": "student",
            "status_for_loan": True
        }

        message_status_code = "Verify if return status code is 200"
        message_body = "Verify if returned body is correct"

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

        message = "Verify authentication class was given"

        self.assertEqual(expected_status_code, response_status_code, message)

    def test_patch_student_status_with_student_token(self):
        base_url = self.BASE_URL + str(self.student.id) + "/"

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.student_token
        )
        response = self.client.patch(path=base_url)

        expected_status_code = 403
        expected_body = {
            "detail": "You do not have permission to perform this action."
        }

        message_status_code = "Verify if return status code is 403"
        message_body = "Verify if permission class only auhtorize colaborators"

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

        message_status_code = "Verify if return status code is 406"
        message_body = "Verify if returned body is correct"

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

        message_status_code = "Verify if return status code is 406"
        message_body = "Verify if returned body is correct"

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
            "id": 2,
            "email": "student@mail.com",
            "username": "student",
            "first_name": "stu",
            "last_name": "dent",
            "is_colaborator": False,
            "status_for_loan": False
        }

        message_status_code = "Verify if return status code is 200"
        message_body = "Verify if returned body is correct"

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
