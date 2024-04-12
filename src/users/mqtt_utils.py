import paho.mqtt.client as mqtt
from django.conf import settings

def publish_command_to_device(device_id, command):
    topic = f"devices/{device_id}/command"
    client = mqtt.Client()
    client.connect(settings.MQTT_BROKER_ADDRESS, settings.MQTT_BROKER_PORT, settings.MQTT_KEEPALIVE_INTERVAL)
    client.publish(topic, command)
    client.disconnect()