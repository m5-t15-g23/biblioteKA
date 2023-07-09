from django.http import HttpResponse


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
