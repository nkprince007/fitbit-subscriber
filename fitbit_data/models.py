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


class BodyFatLog(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='fat_logs')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Body Fat Log'
        verbose_name_plural = 'Body Fat Logs'


class BodyWeightLog(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='weight_logs')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Body Weight Log'
        verbose_name_plural = 'Body Weight Logs'


class HeartRateSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='heart_rate_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Heart Rate Timeseries'
        verbose_name_plural = 'Heart Rate Timeseries'
