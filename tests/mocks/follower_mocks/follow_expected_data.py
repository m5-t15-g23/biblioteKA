def dinamic_self(id, student, book):
    return {
        "id": id,
        "student_id": student.id,
        "student_username": student.username,
        "book_followed_id": book.id,
        "book_followed_title": book.title,
    }
