from books.models import Book


def create_book(book_data, colaborator) -> Book:
    book = Book.objects.create(**book_data)
    book.users.add(colaborator)
    return book
