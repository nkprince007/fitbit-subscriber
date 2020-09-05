from django.contrib.admindocs.urls import urlpatterns
from django.urls import path

from fitbit_auth.views import auth_complete, auth_initialize


urlpatterns = [
    path('login/', auth_initialize),
    path('complete/', auth_complete),
]
