from datetime import datetime, timedelta
from typing import Optional

from django.shortcuts import get_object_or_404

from fitbit_data.exceptions import InvalidPatientIdException, InvalidPeriodException


def format_date(date: datetime, fmt: Optional[str] = '%d/%m/%Y') -> str:
    return date.strftime(fmt)


def get_week_start_date(date):
    return date - timedelta(date.weekday() + 1)


def get_week_end_date(date):
    return date + timedelta(5 - date.weekday())


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


def _convert_dimension(unit_name: str, unit_type: str, value: float):
    if unit_type.lower() == 'duration':
        return value  # milliseconds

    if unit_type.lower() == 'distance':
        if unit_name.upper() == 'EN_US':
            return value * 1609.34  # miles to meters
        else:
            return value * 1000  # kilometers to meters

    if unit_type.lower() == 'elevation':
        if unit_name.upper() == 'EN_US':
            return value * 0.3048  # feet to meters
        else:
            return value  # meters to meters

    if unit_type.lower() in ['height', 'body measurements']:
        if unit_name.upper() == 'EN_US':
            return value * 0.0254  # feet to meters
        else:
            return value / 100  # centimeters to meters

    if unit_type.lower() == 'weight':
        if unit_name.upper() == 'EN_US':
            return value * 0.453592  # pounds to kilograms
        elif unit_name.upper() == 'EN_UK':
            return value * 6.35029  # stones to kilograms
        else:
            return value  # kilograms to kilograms

    if unit_type.lower() == 'liquids':
        if unit_name.upper() == 'EN_US':
            return value * 1000 * 0.0295735  # fluid ounces to millilitres
        else:
            return value  # millilitres to millilitres


def required_calories(user, date=None):
    if date == None:
        activity = user.fb_auth.activity_summary.filter(date=datetime.today())
    else:
        activity = user.fb_auth.activity_summary.filter(date=date)
    if activity.count() == 0:
        return None

    avg_activity_factor = sum(
        [group.activity_factor for group in activity]) / activity.count()
    return user.fb_auth.basal_metabolic_rate * avg_activity_factor
