from django.http import HttpResponse


def dinamic_response(user_data, id):
    return {
        "id": id,
        "email": user_data["email"],
        "username": user_data["username"],
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
    }


def dinamic_self(student):
    return {
        "id": student.id,
        "email": student.email,
        "username": student.username,
        "first_name": student.first_name,
        "last_name": student.last_name,
    }


expected_data = {
    "invalid_expected": {
        "email": [
            "Enter a valid email address."
        ],
        "first_name": [
            "This field is required."
        ],
        "last_name": [
            "Not a valid string."
        ],
        "password": [
            "This field is required."
        ],
        "is_colaborator": [
            "Must be a valid boolean."
        ]
    },
    "email_username_already_in_use": {
        "email": [
            "Email already in use"
        ],
        "username": [
            "Username already in use"
        ]
    },
    "username_password_fileds_required": {
        "username": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ]
    },
    "credentials_not_provided": {
        "detail": "Authentication credentials were not provided."
    },
    "no_active_account_found": {
        "detail": "No active account found with the given credentials"
    },
    "non_permission": {
        "detail": "You do not have permission to perform this action."
    }
}
