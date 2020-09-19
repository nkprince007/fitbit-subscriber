from base64 import b64encode
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from fitbit.exceptions import HTTPUnauthorized
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from fitbit_auth.models import FitbitUser
from fitbit_auth.utils import (LOGGER,
                               create_user_profile,
                               verified_signature_required)


User = get_user_model()


FITBIT_AUTHORIZE_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
FITBIT_API_BASE_URL = 'https://api.fitbit.com/'
FITBIT_SCOPES = [
    'activity',
    'nutrition',
    'heartrate',
    'location',
    'nutrition',
    'profile',
    'settings',
    'sleep',
    'social',
    'weight',
]


def index(request):
    return render(request, 'index.html')


@api_view(('GET',))
def get_profile(request, **kwargs):
    user = get_object_or_404(User, id=kwargs.get('id'))
    try:
        client = user.fb_auth.client
        return Response(client.user_profile_get(user.username).get('user'))
    except FitbitUser.DoesNotExist:
        return Response({'detail': 'Not found.'},
                        status=status.HTTP_404_NOT_FOUND)


def auth_initialize(request):
    params = {
        'response_type': 'code',
        'client_id': settings.FITBIT_CLIENT_ID,
        'scope': ' '.join(FITBIT_SCOPES),
    }
    request = requests.Request(
        'GET', FITBIT_AUTHORIZE_BASE_URL, params=params).prepare()
    return redirect(request.url)


@api_view(['GET'])
def auth_complete(request):
    code = request.GET.get('code')
    url = urljoin(FITBIT_API_BASE_URL, 'oauth2/token')
    token_data = bytes(f'{settings.FITBIT_CLIENT_ID}:'
                       f'{settings.FITBIT_CLIENT_SECRET}', 'utf-8')
    token = b64encode(token_data).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': settings.FITBIT_CLIENT_ID,
        'grant_type': 'authorization_code',
        'code': code
    }
    try:
        credentials = requests.post(url, data=data, headers=headers).json()
        user_id = credentials.get('user_id')
        if not User.objects.filter(username=user_id).exists():
            fitbit_user = create_user_profile(credentials)
        else:
            fitbit_user = User.objects.get(username=user_id).fb_auth
        profile = fitbit_user.client.user_profile_get(user_id).get('user')
    except (HTTPUnauthorized, requests.exceptions.HTTPError, TypeError) as error:
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'profile': profile}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@verified_signature_required
def webhook_listen(request):
    # Subscription verification process
    # Reference: https://dev.fitbit.com/build/reference/web-api/subscriptions/#verify-a-subscriber
    code = request.GET.get('verify')
    if code:
        if code == settings.FITBIT_SUBSCRIBER_VERIFICATION_CODE:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    # TODO: Process notifications in background with celery
    notifications = request.data
    LOGGER.info(notifications)
    # process_notifications.delay(notifications)
    return Response(None, status=status.HTTP_204_NO_CONTENT)
