import paho.mqtt.client as mqtt

from apps.device.devices import DEVICES

def on_connect(client, userdata, rc):
    client.subscribe("devices")
    

def on_message(client, userdata, msg):
    print("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("mosquitto", 1883, 60)
client.connect("localhost", 1883, 60)