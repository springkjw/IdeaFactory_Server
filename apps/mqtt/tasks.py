from datetime import datetime
from .models import Device
from apps.device.devices import DEVICES
from config.mqtt import client as mqttc

def device():
    devices = Device.objects.filter(
        is_active=True,
        expired__lte=datetime.now()
    )

    for device in devices:
        for mac, d in DEVICES.items():
            if d == device.device_id:
                mqttc.publish("device", "{}{}".format(mac, "0"))


    devices.update(
        is_active=False,
        expired=None
    )