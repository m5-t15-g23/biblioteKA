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

        message = "Verify if field loan_date DateField type"

        self.assertTrue(isinstance(result, models.DateField), message)

    def test_is_active_properties(self):
        result = Loan._meta.get_field("is_active").default

        message = "Verify if default value for is_active property is True"

        self.assertTrue(result, message)

    def test_returned_at_properties(self):
        result = Loan._meta.get_field("returned_at")

        message = "Verify if field loan_date DateField type"

        self.assertTrue(isinstance(result, models.DateField), message)
