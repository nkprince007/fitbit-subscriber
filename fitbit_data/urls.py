from django.urls import path

from fitbit_data.views import (get_activity_metrics,
                               get_activity_summary,
                               get_activity_zones,
                               get_body_weight_metrics,
                               get_body_fat_metrics,
                               get_calorie_count,
                               get_heart_rate_zones,
                               get_patient_details,
                               get_patient_ids,
                               get_patients,
                               get_sleep_zones)


urlpatterns = [
    path('patients/', get_patients, name='patients'),
    path('patient_ids/', get_patient_ids, name='patient_ids'),
    path('activity_summary/', get_activity_summary, name='activity_summary'),
    path('patient_details/', get_patient_details, name='patient_details'),
    path('activity_zones/', get_activity_zones, name='activity_zones'),
    path('activity_metrics/', get_activity_metrics, name='activity_metrics'),
    path('calorie_count/', get_calorie_count, name='calorie_count'),
    path('body_weight_metrics/', get_body_weight_metrics,
         name='body_weight_metrics'),
    path('body_fat_metrics/', get_body_fat_metrics, name='body_fat_metrics'),
    path('sleep_zones/', get_sleep_zones, name='sleep_zones'),
    path('heart_rate_zones/', get_heart_rate_zones, name='heart_rate_zones'),
]
