from django.http import HttpResponse
from datetime import datetime as dt


def dinamic_response(response: HttpResponse):
    return {
        "id": response.json()["id"],
        "title": response.json()["title"],
        "author": response.json()["author"],
        "description": response.json()["description"],
        "publication_year": response.json()["publication_year"],
        "page_numbers": response.json()["page_numbers"],
        "language": response.json()["language"],
        "genre": response.json()["genre"],
        "disponibility": response.json()["disponibility"],
    }


def dinamic_self(book):
    date_format = "%Y-%m-%d"
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "publication_year": book.publication_year.strftime(
            date_format
        ),
        "page_numbers": book.page_numbers,
        "language": book.language,
        "genre": book.genre,
        "disponibility": book.disponibility,

    }


expected_data = {
    "invalid_expected": {
        "author": [
            "This field is required."
        ],
        "description": [
            "Not a valid string."
        ],
        "language": [
            "\"english\" is not a valid choice."
        ],
        "genre": [
            "Not a valid string."
        ],
        "copies_number": [
            "This field is required."
        ]
    }
}
