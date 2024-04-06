from rest_framework.serializers import ModelSerializer
from .models import TimeStamp

class TimeStampSerializer(ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = '__all__'