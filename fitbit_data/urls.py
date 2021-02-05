from django.urls import path

from fitbit_data.views import (get_activity_metrics,
                               get_activity_summary,
                               get_activity_zones,
                               get_body_weight_fat_metrics,
                               get_calorie_count,
                               get_patient_details,
                               get_patient_ids)


urlpatterns = [
    path('patient_ids/', get_patient_ids, name='patient_ids'),
    path('activity_summary/', get_activity_summary, name='activity_summary'),
    path('patient_details/', get_patient_details, name='patient_details'),
    path('activity_zones/', get_activity_zones, name='activity_zones'),
    path('activity_metrics/', get_activity_metrics, name='activity_metrics'),
    path('calorie_count/', get_calorie_count, name='calorie_count'),
    path('body_metrics/', get_body_weight_fat_metrics, name='body_metrics'),
]
