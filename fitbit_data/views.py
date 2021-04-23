from datetime import timedelta

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from fitbit_auth.models import FitbitUser, User
from fitbit_auth.serializers import FitbitUserSerializer
from fitbit_data.models import ActivitySummary
from fitbit_data.utils import (get_patient_id,
                               format_date,
                               get_range,
                               get_week_end_date,
                               get_week_start_date)
from fitbit_data.serializers import (HeartRateSummarySerializer,
                                     SleepSummarySerializer)


@user_passes_test(lambda user: user.is_superuser)
def dashboard(request):
    return render(request, 'dashboard.html')


@api_view(('GET',))
def get_patient_ids(request):
    return Response(User.objects.values_list('id', flat=True))


@api_view(('GET',))
def get_patients(request):
    data = FitbitUserSerializer(FitbitUser.objects.all(), many=True).data
    return Response(data)


@api_view(('POST',))
def get_patient_details(request):
    patient = get_object_or_404(User, id=get_patient_id(request))
    try:
        return Response({**patient.fb_auth.profile_data, 'user': patient.id})
    except FitbitUser.DoesNotExist:
        return Response({'detail': 'Not found.'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(('POST', ))
def get_activity_summary(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)
    bmr = fb_user.basal_metabolic_rate

    start_date, end_date = get_range(request)
    start_date, end_date = get_week_start_date(
        start_date), get_week_end_date(end_date)
    summaries = fb_user.activity_summary.filter(
        date__gte=start_date, date__lte=end_date)

    response = []
    date = start_date
    delta = timedelta(days=1)
    while date <= end_date:
        data = {
            'weekDay': date.strftime('%a'),
            'date': format_date(date),
            'weekRange': {
                'start': format_date(get_week_start_date(date)),
                'end': format_date(get_week_end_date(date)),
            },
        }
        try:
            summary = summaries.get(date=date)
            data['physicalActivityLevel'] = (
                summary.data.get('summary').get('caloriesOut') / bmr
                if summary.data and summary.data.get('summary')
                and summary.data.get('summary').get('caloriesOut') else 0)
        except ActivitySummary.DoesNotExist:
            data['physicalActivityLevel'] = None
        finally:
            response.append(data)
        date += delta

    return Response({
        'summaries': response,
        'startDate': format_date(start_date),
        'endDate': format_date(end_date),
    })


@api_view(('POST',))
def get_activity_zones(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)

    start_date, end_date = get_range(request)
    summaries = fb_user.activity_summary.filter(
        date__gte=start_date, date__lte=end_date)

    zones = []
    for summary in summaries:
        data = summary.data.get('summary')
        sedentary = data.get('sedentaryMinutes', 0) / 60
        lightlyActive = data.get('lightlyActiveMinutes', 0) / 60
        fairlyActive = data.get('fairlyActiveMinutes', 0) / 60
        veryActive = data.get('veryActiveMinutes', 0) / 60
        zones.append({
            'date': format_date(summary.date),
            'sedentary': sedentary,
            'lightlyActive': lightlyActive,
            'fairlyActive': fairlyActive,
            'veryActive': veryActive,
            'untracked': 24 - sum([sedentary, lightlyActive, fairlyActive, veryActive]),
        })

    if len(zones) == 0:
        zones = [{
            'date': format_date(end_date),
            # 'Sedentary': 0,
            'Lightly active': 0,
            'Fairly active': 0,
            'Very active': 0,
        }]

    return Response(zones)


@api_view(('POST',))
def get_activity_metrics(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)

    start_date, end_date = get_range(request)
    summaries = fb_user.activity_summary.filter(
        date__gte=start_date, date__lte=end_date)

    metrics = []
    for summary in summaries:
        metrics.append({
            'date': format_date(summary.date),
            'metric': 'Step Count',
            'value': summary.steps,
            'optimal': 8170  # Check 'optimal values.md'
        })
        metrics.append({
            'date': format_date(summary.date),
            'metric': 'Flights climbed',
            'value': summary.flights_climbed,
            'optimal': {'min': 2, 'max': 4}  # Check 'optimal values.md'
        })
        metrics.append({
            'date': format_date(summary.date),
            'metric': 'Distance travelled (m)',
            'value': summary.distance_travelled * 1000,  # km to m
            # Check 'optimal values.md'
            'optimal': {'min': 1.5 * 1609.34, 'max': 3 * 1609.34}
        })
        metrics.append({
            'date': format_date(summary.date),
            'metric': 'Active Duration (min)',
            'value': summary.active_duration,  # min
            # Check 'optimal values.md'
            'optimal': 27
        })

    if len(metrics) == 0:
        metrics = [
            {
                'date': format_date(end_date),
                'metric': metric,
                'value': 0,
            }
            for metric in ['Step Count',
                           'Flights climbed',
                           'Distance travelled (m)',
                           'Active Duration (hrs)']
        ]
    return Response(metrics)


@api_view(('POST',))
def get_calorie_count(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)
    bmr = fb_user.basal_metabolic_rate

    start_date, end_date = get_range(request)
    activity_summaries = fb_user.activity_summary.filter(
        date__gte=start_date, date__lte=end_date).order_by('date')
    food_summaries = fb_user.food_summary.filter(
        date__gte=start_date, date__lte=end_date).order_by('date')

    calories = []
    for food_summary in food_summaries:
        activity_summary = activity_summaries.filter(
            date=food_summary.date).first()
        activity_factor = (activity_summary.activity_factor
                           if activity_summary else 1.2)
        optimal_value = bmr * activity_factor

        calories.append({
            'date': format_date(food_summary.date),
            'current_value': food_summary.data.get('summary').get('calories', 0),
            'optimal_value': optimal_value,
        })
    return Response(calories)


@api_view(('POST',))
def get_body_fat_metrics(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)

    start_date, end_date = get_range(request)
    fat_logs = fb_user.fat_logs.filter(
        date__gte=start_date, date__lte=end_date)

    response_data = []
    for log in fat_logs:
        if log.fat is None:
            continue

        response_data.append({
            'value': log.fat,
            'metric_type': log.source,
            'date': format_date(log.date),
            'metric': 'Body Fat (%)'
        })

    if len(response_data) == 0:
        response_data = [{
            'value': 0,
            'metric_type': 'dummy',
            'date': format_date(end_date),
            'metric': 'Body Fat (%)'
        }]

    return Response(response_data)


@api_view(('POST',))
def get_body_weight_metrics(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)

    start_date, end_date = get_range(request)
    weight_logs = fb_user.weight_logs.filter(
        date__gte=start_date, date__lte=end_date)

    response_data = []
    for log in weight_logs:
        response_data.append({
            'value': log.bmi,
            'metric_type': log.source,
            'date': format_date(log.date),
            'metric': 'Body Mass Index (BMI)',
            'optimal': 28.1,  # check 'optimal values.md'
        })
        response_data.append({
            'value': log.weight,
            'metric_type': log.source,
            'date': format_date(log.date),
            'metric': 'Body Weight (kgs)'
        })

    if len(weight_logs) == 0:
        response_data = [{
            'value': 0,
            'metric_type': 'dummy',
            'date': format_date(end_date),
            'metric': 'Body Mass Index (BMI)'
        }, {
            'value': 0,
            'metric_type': 'dummy',
            'date': format_date(end_date),
            'metric': 'Body Weight (kgs)'
        }]
    return Response(response_data)


@api_view(('POST',))
def get_sleep_zones(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)

    start_date, end_date = get_range(request)
    sleep_logs = fb_user.sleep_summary.filter(
        date__gte=start_date, date__lte=end_date)

    data = SleepSummarySerializer(sleep_logs, many=True).data
    return Response(data)


@api_view(('POST',))
def get_heart_rate_zones(request):
    patient_id = get_patient_id(request)
    fb_user = get_object_or_404(FitbitUser, user_id=patient_id)

    start_date, end_date = get_range(request)
    heart_rate_logs = fb_user.heart_rate_summary.filter(
        date__gte=start_date, date__lte=end_date)

    data = HeartRateSummarySerializer(heart_rate_logs, many=True).data
    return Response(data)
