from datetime import timedelta, datetime
from random import randint

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fitbit_data.utils import get_patient_id, get_period


def dashboard(request):
    return render(request, 'dashboard.html')


@api_view(('POST',))
def get_patient_details(request):
    patient_id = get_patient_id(request)
    return Response({'name': "John Doe", 'age': 23, 'sex': 'Male'})


@api_view(('POST', ))
def get_activity_summary(request):
    period = get_period(request)
    patient_id = get_patient_id(request)

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
    period = get_period(request)
    patient_id = get_patient_id(request)

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


@api_view(('POST',))
def get_calorie_count(request):
    period = min(get_period(request), 30)
    patient_id = get_patient_id(request)

    return Response([
        {
            'date': (datetime.today() - timedelta(i)).strftime('%d/%m/%Y'),
            'current_value': randint(0, 100),
            'optimal_value': randint(0, 100),
        }
        for i in range(period)
    ])
