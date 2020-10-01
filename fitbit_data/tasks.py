from enum import Enum
from typing import Optional

from django.contrib.auth import get_user_model

from fitbit_auth.utils import LOGGER
from fitbit_data.models import (ActivitySummary,
                                FoodSummary,
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


@celery.task
def process_notification(notification):
    user_id = notification.get('ownerId')
    fb_user: Optional[User] = User.objects.filter(username=user_id).first()
    if not fb_user:
        LOGGER.warning('User %s not found. Notification: %s',
                       user_id, notification)
        return

    collection_type = notification.get('collectionType')
    date = notification.get('date')
    api_client: CustomFitbit = fb_user.client
    common_kwargs = {'fb_user': fb_user, 'date': date}

    if collection_type == CollectionType.activities:
        activity_data = api_client.activity_summary(user_id, date)
        ActivitySummary.objects.update_or_create(
            **common_kwargs, defaults={'data': activity_data})

    elif collection_type == CollectionType.foods:
        food_data = api_client.food_summary(user_id, date)
        FoodSummary.objects.update_or_create(
            **common_kwargs, defaults={'data': food_data})
        water_data = api_client.water_summary(user_id, date)
        WaterSummary.objects.update_or_create(
            **common_kwargs, defaults={'data': water_data})

    elif collection_type == CollectionType.sleep:
        sleep_data = api_client.get_sleep(date)
        SleepSummary.objects.update_or_create(
            **common_kwargs, defaults={'data': sleep_data})

    # TODO: Body and fat logs need to be collected
    # elif collection_type == CollectionType.body:
    #     pass

    else:
        LOGGER.warning('Collection type: %s not implemented for storage!')
