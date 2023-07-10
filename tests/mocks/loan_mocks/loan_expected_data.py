def dinamic_response(loan_data, student_data, copy_id, book_title, id):
    return {
        "id": id,
        "loan_date": loan_data["loan_date"],
        "loan_return": loan_data["loan_return"],
        "is_active": loan_data["is_active"],
        "returned_at": loan_data["returned_at"],
        "user_id": student_data.id,
        "user_email": student_data.email,
        "user_username": student_data.username,
        "copy_id": copy_id,
        "book_title": book_title
    }


def dinamic_self(
            loan_data,
            is_active,
            student_data,
            copy_id,
            book_title,
            **kwargs
        ):
    date_formate = "%Y-%m-%d"
    returned_at = kwargs.get("returned_at", None)
    return {
        "id": loan_data.id,
        "loan_date": loan_data.loan_date.strftime(date_formate),
        "loan_return": loan_data.loan_return.strftime(date_formate),
        "is_active": is_active,
        "returned_at": (returned_at.strftime(date_formate)
                        if returned_at is not None
                        else loan_data.returned_at),
        "user_id": student_data.id,
        "user_email": student_data.email,
        "user_username": student_data.username,
        "copy_id": copy_id,
        "book_title": book_title
    }
