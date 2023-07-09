from django.http import HttpResponse


def dinamic_response(response: HttpResponse):
    return {
        "id": response.json()["id"],
        "email": response.json()["email"],
        "username": response.json()["username"],
        "first_name": response.json()["first_name"],
        "last_name": response.json()["last_name"],
    }


def dinamic_self(self):
    return {
        "id": self.student.id,
        "email": self.student.email,
        "username": self.student.username,
        "first_name": self.student.first_name,
        "last_name": self.student.last_name,
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
    "no_active_account_found": {
        "detail": "No active account found with the given credentials"
    },
    "non_permission": {
        "detail": "You do not have permission to perform this action."
    }
}
