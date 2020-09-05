from base64 import b64encode
from urllib.parse import urljoin
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
import fitbit
from fitbit.exceptions import HTTPUnauthorized
import requests


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


def auth_initialize(request):
    params = {
        'response_type': 'code',
        'client_id': settings.FITBIT_CLIENT_ID,
        'scope': ' '.join(FITBIT_SCOPES),
    }
    request = requests.Request(
        'GET', FITBIT_AUTHORIZE_BASE_URL, params=params).prepare()
    return redirect(request.url)


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
        response = requests.post(url, data=data, headers=headers).json()
        access_token = response.get('access_token')
        refresh_token = response.get('refresh_token')
        expires_at = response.get('expires_at')
        user_id = response.get('user_id')
        client = fitbit.Fitbit(settings.FITBIT_CLIENT_ID,
                               settings.FITBIT_CLIENT_SECRET,
                               access_token,
                               refresh_token,
                               expires_at)
        user = client.user_profile_get(user_id)
    except (HTTPUnauthorized, requests.exceptions.HTTPError) as error:
        return JsonResponse({'error': str(error)})
    return JsonResponse({
        'response': response,
        'headers': headers,
        'data': data,
        **user,
    })
