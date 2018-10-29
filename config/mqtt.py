import paho.mqtt.client as mqtt

def on_connect(client, userdata, rc):
    client.subscribe("rfid")
    print('a')

def on_message(client, userdata, msg):
    # Do something
    print(msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)