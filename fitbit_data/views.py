from datetime import timedelta, datetime
from random import randint

from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fitbit_auth.models import FitbitUser
from fitbit_data.utils import get_patient_id, get_period, format_date


def dashboard(request):
    return render(request, 'dashboard.html')


@api_view(('GET',))
def get_patient_ids(request):
    return Response([i+1 for i in range(100)])


@api_view(('POST',))
def get_patient_details(request):
    patient_id = get_patient_id(request)
    return Response({'name': "John Doe", 'age': 23, 'sex': 'Male'})


@api_view(('POST', ))
def get_activity_summary(request):
    period = get_period(request)
    patient_id = get_patient_id(request)

    num_weeks = period // 7
    week_days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    today = datetime.today()
    week_day_index = (today.weekday() + 1) % 7
    last_sun = today - timedelta(7 + week_day_index)
    last_sat = today - timedelta(7 + week_day_index - 6)
    return Response([
        {
            'weekIndex': -week_index,
            'weekDay': week_day,
            'weekRange': {
                'start': format_date(last_sun - timedelta(weeks=week_index)),
                'end': format_date(last_sat - timedelta(weeks=week_index)),
            },
            'value': randint(0, 100),
        }
        for week_index in range(num_weeks)
        for week_day in week_days
    ])


@api_view(('POST',))
def get_activity_zones(request):
    period = get_period(request)
    patient_id = get_patient_id(request)

    return Response([
        {
            'date': format_date(datetime.today() - timedelta(i)),
            'Sedentary': randint(0, 100),
            'Lightly active': randint(0, 100),
            'Fairly active': randint(0, 100),
            'Very active': randint(0, 100),
        }
        for i in range(period)
    ])


@api_view(('POST',))
def get_activity_metrics(request):
    period = get_period(request)
    patient_id = get_patient_id(request)
    metrics = ['Flights climbed',
               'Step Count',
               'Distance travelled (m)',
               'Active Duration (hrs)']

    return Response([
        {
            'date': format_date(datetime.today() - timedelta(i)),
            'metric': metric,
            'value': randint(50, 200)
        }
        for i in range(period)
        for metric in metrics
    ])


@api_view(('POST',))
def get_calorie_count(request):
    period = get_period(request)
    patient_id = get_patient_id(request)

    return Response([
        {
            'date': format_date(datetime.today() - timedelta(i)),
            'current_value': randint(0, 100),
            'optimal_value': randint(0, 100),
        }
        for i in range(period)
    ])


@api_view(('POST',))
def get_body_fat_metrics(request):
    period = get_period(request)
    patient_id = get_patient_id(request)

    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)
    start_date = datetime.today()-timedelta(days=period)
    fat_logs = fb_user.fat_logs.filter(date__gte=start_date)

    response_data = []
    for log in fat_logs:
        response_data.append({
            'value': log.fat,
            'metric_type': log.source,
            'date': format_date(log.date),
            'metric': 'Body Fat (%)'
        })

    return Response(response_data)


@api_view(('POST',))
def get_body_weight_metrics(request):
    period = get_period(request)
    patient_id = get_patient_id(request)

    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)
    start_date = datetime.today()-timedelta(days=period)
    weight_logs = fb_user.weight_logs.filter(date__gte=start_date)

    response_data = []
    for log in weight_logs:
        response_data.append({
            'value': log.bmi,
            'metric_type': log.source,
            'date': format_date(log.date),
            'metric': 'Body Mass Index (BMI)'
        })
        response_data.append({
            'value': log.weight,
            'metric_type': log.source,
            'date': format_date(log.date),
            'metric': 'Body Weight (kgs)'
        })

    return Response(response_data)


@api_view(('POST',))
def get_sleep_zones(request):
    period = get_period(request)
    return Response([
        {
            'date': format_date(datetime.today() - timedelta(i)),
            'asleep': randint(0, 100),
            'awake': randint(0, 100),
            'restless': randint(0, 100),
            'efficiency': randint(0, 100),
        }
        for i in range(period)
    ])
