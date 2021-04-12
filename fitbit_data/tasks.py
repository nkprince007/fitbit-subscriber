from datetime import datetime
from enum import Enum
from typing import Optional

from django.contrib.auth import get_user_model

from admin import LOGGER
from fitbit_auth.models import FitbitUser
from fitbit_data.models import (ActivitySummary,
                                BodyFatLog,
                                BodyWeightLog,
                                FoodSummary, HeartRateSummary,
                                SleepSummary,
                                WaterSummary)
from subscriber import celery
from subscriber.fitbit import CustomFitbit


User = get_user_model()


class CollectionType(str, Enum):
    # Collection types are defined in subscription components
    # Reference: https://dev.fitbit.com/build/reference/web-api/subscriptions/
    activities = 'activities'
    body = 'body'
    foods = 'foods'
    sleep = 'sleep'
    profile = 'profile'


@celery.task
def add(first, second):
    return first + second


@celery.task
def process_additional_data(fb_user_id: int, date: str = 'today'):
    fb_user = FitbitUser.objects.get(id=fb_user_id)
    api_client = fb_user.client
    data = api_client.time_series(
        'activities/heart',
        base_date=date,
        period='1d'
    ).get('activities-heart')

    if date == 'today':
        if len(data) > 0 and data[0].get('dateTime'):
            date = data[0].get('dateTime')
        else:
            now = datetime.today()
            date = '%s-%s-%s' % (now.year, now.month, now.date)

    HeartRateSummary.objects.update_or_create(
        fb_user=fb_user, date=date, defaults={'data': data})


@celery.task
def process_notification(notification):
    user_id = notification.get('ownerId')
    user: Optional[User] = User.objects.filter(username=user_id).first()
    if not user or not user.fb_auth:
        LOGGER.warning('User %s not found. Notification: %s',
                       user_id, notification)
        return

    fb_user: FitbitUser = user.fb_auth
    collection_type = notification.get('collectionType')
    date = notification.get('date')
    api_client: CustomFitbit = fb_user.client
    common_kwargs = {'fb_user': fb_user, 'date': date}

    if collection_type == CollectionType.activities:
        activity_data = api_client.get_activity_summary(user_id, date)
        ActivitySummary.objects.update_or_create(
            **common_kwargs, defaults={'data': activity_data})
        process_additional_data.delay(fb_user.id, date)

    elif collection_type == CollectionType.foods:
        food_data = api_client.get_food_summary(user_id, date)
        FoodSummary.objects.update_or_create(
            **common_kwargs, defaults={'data': food_data})
        water_data = api_client.get_water_summary(user_id, date)
        WaterSummary.objects.update_or_create(
            **common_kwargs, defaults={'data': water_data})

    elif collection_type == CollectionType.sleep:
        sleep_data = api_client.get_sleep(datetime.fromisoformat(date))
        SleepSummary.objects.update_or_create(
            **common_kwargs, defaults={'data': sleep_data})

    elif collection_type == CollectionType.body:
        body_fat_data = api_client.get_body_fat_logs(user_id, date)
        BodyFatLog.objects.update_or_create(
            **common_kwargs, defaults={'data': body_fat_data})
        body_weight_data = api_client.get_body_weight_logs(user_id, date)
        BodyWeightLog.objects.update_or_create(
            **common_kwargs, defaults={'data': body_weight_data})

    elif collection_type == CollectionType.profile:
        fb_user.refresh_profile()

    else:
        LOGGER.warning('Collection type: %s not implemented for storage!')
