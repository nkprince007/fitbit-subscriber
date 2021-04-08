from typing import Optional

from cached_property import cached_property_with_ttl
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from subscriber.fitbit import CustomFitbit


User = get_user_model()


class FitbitUser(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='fb_auth')
    profile_data = models.JSONField(default=dict)
    access_token = models.TextField()
    refresh_token = models.TextField()
    scope = models.TextField()
    expires_at = models.DateTimeField(default=timezone.now)

    @cached_property_with_ttl(ttl=5 * 60)  # cache invalidates after 5 minutes
    def basal_metabolic_rate(self) -> Optional[float]:
        profile = self.profile_data
        gender = profile.get('gender').upper()
        height = profile.get('height')
        weight = profile.get('weight')
        age = profile.get('age')
        gender_factor = 5
        if gender == 'FEMALE':
            gender_factor = -161
        return 10 * weight + 6.25 * height - 5 * age + gender_factor

    @property
    def client(self) -> CustomFitbit:
        def update_token(token):
            print(update_token)
            self.access_token = token.get('access_token')
            self.refresh_token = token.get('refresh_token')
            self.expires_at = timezone.now() + (
                timezone.timedelta(seconds=token.get('expires_in')))
            self.save()

        return CustomFitbit(settings.FITBIT_CLIENT_ID,
                            settings.FITBIT_CLIENT_SECRET,
                            access_token=self.access_token,
                            refresh_token=self.refresh_token,
                            expires_at=self.expires_at.timestamp(),
                            refresh_cb=update_token,
                            system='METRIC')

    def __str__(self) -> str:
        return self.user.username
