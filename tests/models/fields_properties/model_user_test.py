from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    def test_email_properties(self):
        result = User._meta.get_field("email").unique
        message = "Verify if email field is set with unique property as True"

        self.assertTrue(result, message)

    def test_username_properties(self):
        result_unique = User._meta.get_field("username").unique
        result_max_length = User._meta.get_field("username").max_length

        expected = 150

        message_unique = ("Verify if username field is "
                          "set with unique property as True")
        message_max_length = (f"Verify if username field has "
                              "property max_length as {expected}")

        self.assertTrue(result_unique, message_unique)
        self.assertEqual(expected, result_max_length, message_max_length)

    def test_first_and_last_name_properties(self):
        result_first_name = User._meta.get_field("first_name").max_length
        result_last_name = User._meta.get_field("last_name").max_length

        expected = 150

        message_first_name = (f"Verify if first_name field has "
                              "property max_length as {expected}")
        message_last_name = (f"Verify if last_name field has "
                             "property max_length as {expected}")

        self.assertEqual(expected, result_first_name, message_first_name)
        self.assertEqual(expected, result_last_name, message_last_name)

    def test_is_colaborator_properties(self):
        result = User._meta.get_field("is_colaborator").default
        message = "Verify is is_colaborator field default is False"

        self.assertFalse(result, message)

    def test_status_for_laon_properties(self):
        result = User._meta.get_field("status_for_loan").default
        message = "Verify is status_for_loan field default is True"

        self.assertTrue(result, message)
