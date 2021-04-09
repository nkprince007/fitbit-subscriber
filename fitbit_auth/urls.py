from django.urls import path, re_path

from fitbit_auth.views import (auth_complete,
                               auth_login,
                               auth_logout,
                               auth_initialize,
                               get_profile)


urlpatterns = [
    re_path(r'users/(?P<id>\w+)/', get_profile, name='get-user-profile'),
    path('login/', auth_login, name='login'),
    path('logout/', auth_logout, name='logout'),
    path('fitbit-login/', auth_initialize, name='login-fitbit'),
    path('complete/', auth_complete, name='login-fitbit-complete'),
]
