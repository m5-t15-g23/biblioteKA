from django.test import TestCase
from copies.models import Copy


class CopyModelTest(TestCase):
    def test_is_avaliable_properties(self):
        result_null = Copy._meta.get_field("is_avaliable").null
        result_default = Copy._meta.get_field("is_avaliable").default

        message_null = "Verify if is_avaliable null property is True"
        message_default = "Verify if is_avaliable default property is True"

        self.assertTrue(result_null, message_null)
        self.assertTrue(result_default, message_default)
