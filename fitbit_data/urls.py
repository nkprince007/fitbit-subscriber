from django.urls import path

from fitbit_data.views import get_activity_summary, get_activity_zones, get_patient_details


urlpatterns = [
    path('activity_summary/', get_activity_summary, name='activity_summary'),
    path('patient_details/', get_patient_details, name='patient_details'),
    path('activity_zones/', get_activity_zones, name='activity_zones'),
]
