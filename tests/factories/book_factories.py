from books.models import Book


def create_book(book_data) -> Book:
    book = Book.objects.create(**book_data)

    return book
