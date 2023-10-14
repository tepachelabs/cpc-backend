from rest_framework import exceptions
from rest_framework.response import Response


class APIException(exceptions.APIException):
    def __init__(self, detail=None, code=None, status_code=None):
        super().__init__(detail, code)
        if status_code is not None:
            self.status_code = status_code

    @property
    def response(self):
        response_data = {
            "custom_error_code": self.default_code,
            "error_message": self.default_detail,
        }

        return Response(response_data, status=self.status_code)
