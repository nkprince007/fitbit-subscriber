from base64 import b64encode
from fitbit_auth.serializers import FitbitUserSerializer
from hashlib import sha1
import hmac

from django.conf import settings
from django.http.response import Http404
from django.utils import timezone
from ipware import get_client_ip

from admin import LOGGER
from fitbit_auth.models import FitbitUser, User


def verified_signature_required(function):
    def wrapper(request, *args, **kwargs):
        signature = request.META.get('HTTP_X_FITBIT_SIGNATURE')
        if signature:
            key = bytes(f'{settings.FITBIT_CLIENT_SECRET}&', 'utf-8')
            hashed = hmac.new(key, request.body, sha1)
            computed_signature = b64encode(hashed.digest())
            if computed_signature != signature.encode('utf-8'):
                ip_addr, _ = get_client_ip(request)
                LOGGER.warning('Suspicious "updates" notification from IP: %s',
                               ip_addr)
                raise Http404
        return function(request, *args, **kwargs)
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


def add_subscription(fitbit_user: FitbitUser):
    client = fitbit_user.client
    return client.subscription(fitbit_user.user.username, None)


def create_user_profile(credentials: dict):
    access_token = credentials.get('access_token')
    refresh_token = credentials.get('refresh_token')
    expires_at = timezone.now() + (
        timezone.timedelta(seconds=credentials.get('expires_in')))
    scope = credentials.get('scope')
    user_id = credentials.get('user_id')
    user, _ = User.objects.get_or_create(username=user_id)
    data = {
        'scope': scope,
        'refresh_token': refresh_token,
        'access_token': access_token,
        'expires_at': expires_at,
    }
    fitbit_user, created = FitbitUser.objects.update_or_create(
        user=user, defaults=data)
    profile = fitbit_user.client.user_profile_get(user_id).get('user')
    fitbit_user.profile_data = profile
    fitbit_user.save()
    if created:
        add_subscription(fitbit_user)
    return fitbit_user
