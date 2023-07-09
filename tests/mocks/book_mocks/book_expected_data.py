from datetime import datetime as dt


def dinamic_response(book_data, id):
    return {
        "id": id,
        "title": book_data["title"],
        "author": book_data["author"],
        "description": book_data["description"],
        "publication_year": str(dt.now().date()),
        "page_numbers": book_data["page_numbers"],
        "language": book_data["language"],
        "genre": book_data["genre"],
        "disponibility": True,
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
