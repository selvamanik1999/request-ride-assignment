from rest_framework.exceptions import APIException
from rest_framework import status


class SQLException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code:
            self.status_code = status_code
