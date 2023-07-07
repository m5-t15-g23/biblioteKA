from rest_framework.exceptions import APIException


class StudentLoanException(APIException):
    status_code = 406
    default_code = "service_unavailable"
