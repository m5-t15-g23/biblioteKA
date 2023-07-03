from django.test import TestCase
from django.db import models
from datetime import datetime

from books.models import Book


class BookModelTest(TestCase):
    def test_title_properties(self):
        result_title = Book._meta.get_field("title").max_length

        expected = 255

        message_title = (f"Verify if title field has property "
                         "max_length as {expected}")

        self.assertEqual(expected, result_title, message_title)

    def test_author_properties(self):
        result = Book._meta.get_field("author").max_length

        expected = 255

        message = (f"Verify if author field has property "
                   "max_length as {expected}")

        self.assertEqual(expected, result, message)

    def test_description_properties(self):
        result = Book._meta.get_field("description")
        message = "Verify if description field type if TextField"

        self.assertTrue(isinstance(result, models.TextField), message)

    def test_publication_year_properties(self):
        format_date = "%d/%m/%Y"

        result_null = Book._meta.get_field("publication_year").null
        result_default = Book._meta.get_field(
            "publication_year"
        ).default.strftime(format_date)

        expected = datetime.now().strftime(format_date)

        message_null = "Verify if publication_yean null property is True"
        message_default = (f"Verify if publication_yean default property"
                           " is {expected}")

        self.assertTrue(result_null, message_null)
        self.assertEqual(expected, result_default, message_default)

    def test_page_numbers_properties(self):
        result_page_numbers = Book._meta.get_field("page_numbers")

        message_page_numbers = "Verify if page_numbers field type if TextField"

        self.assertTrue(
            isinstance(result_page_numbers, models.IntegerField),
            message_page_numbers
        )

    def test_language_properties(self):
        result_choices = Book._meta.get_field("language").choices
        result_choices = [choice[0] for choice in result_choices]
        result_default = Book._meta.get_field("language").default

        expected_choices = [
            "english",
            "portuguese",
            "spenish",
            "french",
            "italian",
            "german",
            "not informed"
        ]
        expected_default = "not informed"

        message_choices = (f"Verify if language field choices"
                           " property is {expected_choices}")
        message_default = (f"Verify if language field default"
                           " property is {expected_default}")

        for choice in expected_choices:
            self.assertIn(choice, result_choices, message_choices)
        self.assertEqual(expected_default, result_default, message_default)

    def test_genre_properties(self):
        result = Book._meta.get_field("genre").max_length

        expected = 255

        message = (f"Verify if genre field has property "
                   "max_length as {expected}")

        self.assertEqual(expected, result, message)

    def test_disponibility_properties(self):
        result_null = Book._meta.get_field("disponibility").null
        result_default = Book._meta.get_field("disponibility").default

        message_null = "Verify if disponibility null property is True"
        message_default = "Verify if disponibility default property is True"

        self.assertTrue(result_null, message_null)
        self.assertTrue(result_default, message_default)

    def test_copies_number_properties(self):
        result = Book._meta.get_field("copies_number")

        message = "Verify if copies_number field type if TextField"

        self.assertTrue(isinstance(result, models.IntegerField), message)
