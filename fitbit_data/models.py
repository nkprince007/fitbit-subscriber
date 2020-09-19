from django.db import models

from fitbit_auth.models import FitbitUser


class ActivitySummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='activity_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)


class SleepSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='sleep_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)


class FoodSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='food_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)


class WaterSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='water_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)


# TODO: Implementing body weight and fat logs
