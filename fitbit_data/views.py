from datetime import timedelta, datetime
from random import randint

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fitbit_data.exceptions import InvalidPatientIdException, InvalidPeriodException


def dashboard(request):
    return render(request, 'dashboard.html')


@api_view(('POST',))
def get_patient_details(request):
    patient_id = request.data.get('patientId')
    try:
        patient_id = int(patient_id)
    except (ValueError, TypeError) as err:
        raise InvalidPatientIdException()
    return Response({'name': "John Doe", 'age': 23, 'sex': 'Male'})


@api_view(('POST', ))
def get_activity_summary(request):
    period = request.data.get('period')
    try:
        period = int(period)
    except (ValueError, TypeError):
        raise InvalidPeriodException()

    patient_id = request.data.get('patientId')
    try:
        patient_id = int(patient_id)
    except (ValueError, TypeError):
        raise InvalidPatientIdException()

    num_weeks = period // 7
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return Response([
        {
            'weekIndex': -i,
            'weekDay': week_day,
            'value': randint(0, 100),
        }
        for i in range(num_weeks)
        for week_day in week_days
    ])


@api_view(('POST',))
def get_activity_zones(request):
    period = request.data.get('period')
    try:
        period = int(period)
    except (ValueError, TypeError):
        raise InvalidPeriodException()

    patient_id = request.data.get('patientId')
    try:
        patient_id = int(patient_id)
    except (ValueError, TypeError):
        raise InvalidPatientIdException()

    return Response([
        {
            'date': (datetime.today() - timedelta(i)).strftime('%d/%m/%Y'),
            'Sedentary': randint(0, 100),
            'Lightly active': randint(0, 100),
            'Fairly active': randint(0, 100),
            'Very active': randint(0, 100),
        }
        for i in range(period)
    ])
