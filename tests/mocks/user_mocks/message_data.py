def message_status_code(status_code: int) -> str:
    return f"Verify if returned status_code is {status_code}"


message_data = {
    "message_body_is_correct": "Verify if returned body is correct",
    "non_give_authentication_class": "Verify authentication class was given",
    "colaborator_authorization": ("Verify if permission class only"
                                  " auhtorize colaborators")
}
