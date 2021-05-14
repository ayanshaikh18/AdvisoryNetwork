from rest_framework import serializers

from api.models import Advisor, Booking


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('name', 'photo')

    name = serializers.CharField(max_length=255, required=True, write_only=True)
    photo = serializers.CharField(max_length=1000, required=True, write_only=True)


class AdviserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('id', 'name', 'photo')
