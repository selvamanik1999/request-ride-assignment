from django.conf import settings
from django.db import models

from ride_api.constants import ASSET_CHOICES, SENSITIVE_CHOICES, TRAVEL_MEDIUM_CHOICES


class Requester(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source = models.CharField(max_length=1000)
    destination = models.CharField(max_length=1000)
    pick_up_time = models.DateTimeField()
    is_flexible_time = models.BooleanField(default=False)
    asset_count = models.IntegerField()
    asset_type = models.CharField(choices=ASSET_CHOICES, max_length=1000)
    sensitive = models.CharField(choices=SENSITIVE_CHOICES, max_length=1000)
    to_deliver_name = models.CharField(max_length=1000)
    to_deliver_phone_no = models.CharField(max_length=10)
    rider_assigned = models.ForeignKey("Rider", unique=True, on_delete=models.CASCADE, null=True)


class Rider(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source = models.CharField(max_length=1000)
    destination = models.CharField(max_length=1000)
    pick_up_time = models.DateTimeField()
    is_flexible_time = models.BooleanField(default=False)
    travel_medium = models.CharField(choices=TRAVEL_MEDIUM_CHOICES, max_length=1000)
    asset_count = models.IntegerField()
