from django.conf import settings
from django.utils import timezone
from fitbit import Fitbit

from fitbit_auth.models import FitbitUser, User


def create_user_profile(credentials: dict):
    access_token = credentials.get('access_token')
    refresh_token = credentials.get('refresh_token')
    expires_at = timezone.now() + (
        timezone.timedelta(seconds=credentials.get('expires_in')))
    scope = credentials.get('scope')
    user_id = credentials.get('user_id')
    client = Fitbit(settings.FITBIT_CLIENT_ID,
                    settings.FITBIT_CLIENT_SECRET,
                    access_token,
                    refresh_token,
                    expires_at.timestamp())
    profile = client.user_profile_get(user_id).get('user')
    user = User.objects.create(
        username=profile.get('encodedId'),
        first_name=profile.get('firstName'),
        last_name=profile.get('lastName'))
    return FitbitUser.objects.create(user=user,
                                     scope=scope,
                                     refresh_token=refresh_token,
                                     access_token=access_token,
                                     expires_at=expires_at)
