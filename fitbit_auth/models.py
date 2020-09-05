from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from fitbit.api import Fitbit


User = get_user_model()


class FitbitUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    scope = models.TextField()
    expires_at = models.DateTimeField(default=timezone.now)

    @property
    def client(self):
        client = Fitbit(settings.FITBIT_CLIENT_ID,
                        settings.FITBIT_CLIENT_SECRET,
                        self.access_token,
                        self.refresh_token,
                        self.expires_at.timestamp())
        return client
        # token = client.client.refresh_token()
        # self.access_token = token.access_token
        # self.refresh_token = token.refresh_token
        # self.save()
        # return client
