from rest_framework.serializers import ModelSerializer

from fitbit_data.models import HeartRateSummary, SleepSummary


class HeartRateSummarySerializer(ModelSerializer):
    class Meta:
        fields = ('data', 'date')
        model = HeartRateSummary


class SleepSummarySerializer(ModelSerializer):
    class Meta:
        fields = ('data', 'date')
        model = SleepSummary
