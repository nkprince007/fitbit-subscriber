from datetime import datetime
from typing import Optional

from fitbit_data.exceptions import InvalidPatientIdException, InvalidPeriodException


def format_date(date: datetime, fmt: Optional[str] = '%d/%m/%Y') -> str:
    return date.strftime(fmt)


def get_patient_id(request):
    patient_id = request.data.get('patientId')
    try:
        return int(patient_id)
    except (ValueError, TypeError) as err:
        raise InvalidPatientIdException()


def get_period(request):
    period = request.data.get('period')
    try:
        return int(period)
    except (ValueError, TypeError):
        raise InvalidPeriodException()
