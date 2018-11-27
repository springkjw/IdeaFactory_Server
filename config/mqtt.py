import paho.mqtt.client as mqtt

def on_connect(client, userdata, rc):
    client.subscribe("rfid")

def on_message(client, userdata, msg):
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mosquitto", 1883, 60)