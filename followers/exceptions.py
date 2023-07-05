from rest_framework.exceptions import APIException


class BookAlreadyFollowed(APIException):
    status_code = 409
    default_code = "service_unavailable"