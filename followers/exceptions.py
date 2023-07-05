from rest_framework.exceptions import APIException


class FollowExceptions(APIException):
    status_code = 409
    default_code = "service_unavailable"


class FollowTableEmpty(APIException):
    status_code = 404
    default_code = "service_unavailable"