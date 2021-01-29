from fitbit_data.exceptions import InvalidPatientIdException, InvalidPeriodException
from random import randint

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
