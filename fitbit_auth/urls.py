from django.urls import path, re_path

from fitbit_auth.views import auth_complete, auth_initialize, get_profile


urlpatterns = [
    re_path(r'users/(?P<id>\w+)/', get_profile),
    path('login/', auth_initialize),
    path('complete/', auth_complete),
]
