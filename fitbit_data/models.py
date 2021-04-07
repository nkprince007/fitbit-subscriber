from collections import Counter

from django.db import models

from fitbit_auth.models import FitbitUser


class ActivitySummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='activity_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    @property
    def steps(self):
        summary = self.data.get('summary')
        if not summary:
            return 0
        return summary.get('steps', 0)

    @property
    def flights_climbed(self):
        summary = self.data.get('summary')
        if not summary:
            return 0
        return summary.get('floors', 0)

    @property
    def active_duration(self):
        summary = self.data.get('summary')
        if not summary:
            return 0
        duration = summary.get('veryActiveMinutes', 0)
        duration += summary.get('fairlyActiveMinutes', 0)
        duration += summary.get('lightlyActiveMinutes', 0)
        return duration

    @property
    def distance_travelled(self):
        summary = self.data.get('summary')
        if not summary:
            return 0
        distances = summary.get('distances')
        for distance in distances:
            if distance.get('activity') == 'total':
                return distance.get('distance')
        return 0

    @property
    def activity_factor(self):
        summary = self.data.get('summary')
        if not summary:
            return 1.2  # assuming sedentary

        sedentary = summary.get('sedentaryMinutes')
        very_active = summary.get('veryActiveMinutes')
        fairly_active = summary.get('fairlyActiveMinutes')
        lightly_active = summary.get('lightlyActiveMinutes')
        max_time_spent = max(sedentary, very_active,
                             fairly_active, lightly_active)
        if max_time_spent == sedentary:
            return 1.2
        elif max_time_spent == lightly_active:
            return 1.375
        elif max_time_spent == fairly_active:
            return 1.725
        elif max_time_spent == very_active:
            return 1.9
        else:
            return 1.55

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Activity Summary'


class SleepSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='sleep_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Sleep Summary'


class FoodSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='food_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Food Summary'


class WaterSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='water_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Water Summary'


class BodyFatLog(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='fat_logs')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    @property
    def source(self):
        logs = self.data.get('fat')
        if len(logs) == 0:
            return None
        sources = list(map(lambda log: log.get('source'), logs))
        try:
            return Counter(sources).most_common(1)[0][0]
        except IndexError:
            return None

    @property
    def fat(self):
        logs = self.data.get('fat')
        if len(logs) == 0:
            return None
        fat_percents = list(map(lambda log: log.get('fat'), logs))
        return sum(fat_percents) / len(fat_percents)

    class Meta:
        ordering = ['date']
        verbose_name = 'Body Fat Log'
        verbose_name_plural = 'Body Fat Logs'


class BodyWeightLog(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='weight_logs')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    @property
    def bmi(self):
        logs = self.data.get('weight')
        if len(logs) == 0:
            return None
        bmis = list(map(lambda log: log.get('bmi'), logs))
        return sum(bmis) / len(bmis)

    @property
    def source(self):
        logs = self.data.get('weight')
        if len(logs) == 0:
            return None
        sources = list(map(lambda log: log.get('source'), logs))
        try:
            return Counter(sources).most_common(1)[0][0]
        except IndexError:
            return None

    @property
    def weight(self):
        logs = self.data.get('weight')
        if len(logs) == 0:
            return None
        weights = list(map(lambda log: log.get('weight'), logs))
        return sum(weights) / len(weights)

    class Meta:
        ordering = ['date']
        verbose_name = 'Body Weight Log'
        verbose_name_plural = 'Body Weight Logs'


class HeartRateSummary(models.Model):
    fb_user = models.ForeignKey(FitbitUser,
                                on_delete=models.CASCADE,
                                related_name='heart_rate_summary')
    date = models.DateField(default=None)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['date']
        verbose_name = 'Heart Rate Timeseries'
        verbose_name_plural = 'Heart Rate Timeseries'
