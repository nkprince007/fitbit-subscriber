from rest_framework.serializers import ModelSerializer

from fitbit_data.models import HeartRateSummary


class HeartRateSummarySerializer(ModelSerializer):
    class Meta:
        fields = ('data', 'date')
        model = HeartRateSummary
