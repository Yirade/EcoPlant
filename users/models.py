# users/models.py

from django.db import models
from django.contrib.auth.models import User
import uuid

def generate_api_key():
    return uuid.uuid4().hex

class Device(models.Model):
    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True, default=generate_api_key)
    owner = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.device_id)
    
class SensorData(models.Model):
    device = models.ForeignKey(Device, related_name='sensor_data', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    # Add here other fields for the data that your device collects

    def __str__(self):
        return f"{self.device.name} {self.timestamp}"