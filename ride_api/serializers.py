from django.utils import timezone
from rest_framework import serializers

from ride_api.models import Requester, Rider


class RequesterSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)  # status - calculated field

    def get_status(self, row):
        return "PENDING" if timezone.now() < row.pick_up_time else "EXPIRED"

    class Meta:
        model = Requester
        fields = '__all__'
        read_only_fields = ('user',)  # Add this


class RequesterApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Requester
        fields = ('rider_assigned',)
        read_only_fields = ('user',)  # Add this


class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = '__all__'
        read_only_fields = ('user',)  # Add this


class RiderMatchRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    source = serializers.CharField(max_length=1000)
    destination = serializers.CharField(max_length=1000)
    pick_up_time = serializers.DateTimeField()
    asset_count = serializers.IntegerField()
    to_deliver_name = serializers.CharField(max_length=1000)
    to_deliver_phone_no = serializers.CharField(max_length=10)
    rider_id = serializers.IntegerField()
    rider_assigned_id = serializers.IntegerField()
    rider_assigned_status = serializers.SerializerMethodField(read_only=True)

    def get_rider_assigned_status(self, row):
        return "APPLIED" if row['rider_assigned_id'] else "NOT_APPLIED"
