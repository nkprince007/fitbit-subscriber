from rest_framework.serializers import ModelSerializer

from fitbit_auth.models import FitbitUser


class FitbitUserSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'profile_data')
        model = FitbitUser
