from base64 import b64encode
from urllib.parse import urljoin
import traceback


from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib import messages
from django.contrib.messages.api import get_messages
from django.shortcuts import get_object_or_404, redirect, render
from fitbit.exceptions import HTTPUnauthorized
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from fitbit_auth.models import FitbitUser
from fitbit_auth.utils import create_user_profile, verified_signature_required
from fitbit_data.tasks import process_notification
from fitbit_data.views import dashboard


User = get_user_model()


FITBIT_AUTHORIZE_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
FITBIT_API_BASE_URL = 'https://api.fitbit.com/'
FITBIT_SCOPES = [
    'activity',
    'heartrate',
    # 'location',  # not required
    'nutrition',
    'profile',  # required for subscriptions, block all other info collection manually
    'settings',  # required for subscriptions, block all other info collection manually
    'sleep',
    # 'social',  # not required
    'weight',
]


def index(request):
    if request.user and request.user.is_authenticated and request.user.is_superuser:
        return redirect(dashboard)

    return render(request,
                  'index.html',
                  context={'messages': get_messages(request)})


@api_view(('GET',))
def get_profile(request, **kwargs):
    user = get_object_or_404(User, id=kwargs.get('id'))
    try:
        client = user.fb_auth.client
        return Response(client.user_profile_get(user.username).get('user'))
    except FitbitUser.DoesNotExist:
        return Response({'detail': 'Not found.'},
                        status=status.HTTP_404_NOT_FOUND)


def auth_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    messages.warning(
        request, 'Unable to login with given credentials. Please try again.')
    return redirect(index)


def auth_logout(request):
    logout(request)
    return redirect(index)


@user_passes_test(lambda user: user.is_superuser)
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
        fitbit_user = create_user_profile(credentials)
        profile = fitbit_user.client.user_profile_get(user_id).get('user')
    except (HTTPUnauthorized, requests.exceptions.HTTPError, TypeError) as error:
        tb = traceback.format_exc()
        return Response({'error': tb}, status=status.HTTP_400_BAD_REQUEST)
    return redirect(dashboard)


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

    for notification in request.data:
        process_notification.delay(notification)
    return Response(None, status=status.HTTP_204_NO_CONTENT)
