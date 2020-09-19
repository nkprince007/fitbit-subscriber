from django.db import models

from fitbit_auth.models import FitbitUser


class ActivitySummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='activity_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = 'Activity Summary'


class SleepSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='sleep_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = 'Sleep Summary'


class FoodSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='food_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = 'Food Summary'


class WaterSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='water_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = 'Water Summary'


# TODO: Implementing body weight and fat logs
