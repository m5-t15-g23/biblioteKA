from django.test import TestCase
from copies.models import Copy


class CopyModelTest(TestCase):
    def test_status_for_loan_properties(self):
        result_null = Copy._meta.get_field("status_for_loan").null
        result_default = Copy._meta.get_field("status_for_loan").default

        message_null = "Verify if status_for_loan null property is True"
        message_default = "Verify if status_for_loan default property is True"

        self.assertTrue(result_null, message_null)
        self.assertTrue(result_default, message_default)
