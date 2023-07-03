from django.test import TestCase
from datetime import datetime, timedelta

from users.models import User
from books.models import Book
from copies.models import Copy
from loans.models import Loan

from faker import Faker
from random import randint


class RelationsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        fake = Faker()

        cls.user_colaborator = User.objects.create_superuser(
            email="usercolaborator@mail.com",
            username="usercolaborator",
            password="1234",
        )
        cls.user_colaborator_two = User.objects.create_user(
            email="usercolaboratortwo@mail.com",
            username="usercolaboratortwo",
            password="1234",
        )
        cls.user_student = User.objects.create_user(
            email="userstudent@mail.com",
            username="userstudent",
            password="1234",
        )

        cls.books = [
            Book.objects.create(
                title=fake.name(),
                author=fake.name(),
                page_numbers=randint(250, 500),
                genre="fiction",
                copies_number=2
            ).user.set([cls.user_colaborator, cls.user_colaborator_two])
            for _ in range(5)
        ]

        cls.book = Book.objects.all().first()

        cls.book_copies = [Copy.objects.create(book=cls.book)
                           for _ in range(2)]

        cls.copy = Copy.objects.all().first()

        cls.loans = [Loan.objects.create(
            loan_return=datetime.now() + timedelta(days=30),
            user=cls.user_student,
            copy=cls.copy
        ) for _ in range(2)]

        cls.loan = Loan.objects.all().first()

    def test_if_a_colaborator_can_have_many_books(self):
        colaborator_books = self.user_colaborator.books

        self.assertEqual(len(self.books), colaborator_books.count())

    def test_if_a_book_can_have_many_colaborators(self):
        book = Book.objects.all().first()

        self.assertTrue(bool(book.user.count() > 1))

    def test_if_a_book_can_have_many_copies(self):
        book = self.book

        self.assertTrue(len(book.copy.all()) > 1)

    def test_if_a_copie_can_have_a_book(self):
        copy = self.copy
        book = self.book

        self.assertIs(copy.book.id, book.id)

    def test_if_a_copie_can_have_many_loans(self):
        copy = self.copy

        self.assertTrue(len(copy.loans.all()) > 1)

    def test_if_a_loan_can_have_a_copy(self):
        loan = self.loan
        copy = self.copy

        self.assertIs(loan.copy.id, copy.id)

    def test_if_a_student_can_have_many_loans(self):
        student = self.user_student

        self.assertTrue(len(student.loans.all()) > 1)

    def test_if_a_loan_can_have_a_student(self):
        loan = self.loan
        student = self.user_student

        self.assertIs(loan.user.id, student.id)
