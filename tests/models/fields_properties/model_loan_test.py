from django.test import TestCase
from django.db import models

from loans.models import Loan


class LoanModelTest(TestCase):
    def test_loan_date_properties(self):
        result = Loan._meta.get_field("loan_date").auto_now_add

        message = "Verify if field loan_date auto_now_add property is True"

        self.assertTrue(result, message)

    def test_loan_return_properties(self):
        result = Loan._meta.get_field("loan_return")

        message = "Verify if field loan_date DateTimeField type"

        self.assertTrue(isinstance(result, models.DateTimeField), message)
