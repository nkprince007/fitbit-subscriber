from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidPatientIdException(APIException):
    default_detail = 'Missing or invalid `patientId`'
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidRangeException(APIException):
    default_detail = 'Missing or invalid `range`'
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidPeriodException(APIException):
    default_detail = 'Missing or invalid `period`'
    status_code = status.HTTP_400_BAD_REQUEST
