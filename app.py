from datetime import datetime
import requests
import paho.mqtt.client as mqtt
from apps.device.devices import DEVICES
# from apps.mqtt.models import Device
import json

api_ip = 'https://ideafactory.kaist.ac.kr/api/getReservationForTag'
auth_user_result = {
    "return": True,
    "msg": "nonbooking eqipment",
    "data":{
        "res_id":None,
        "res_ef_no":"IF025",
        "res_ur_name":"홍길동",
        "res_start_dt":None,
        "res_end_dt":None
    }
}
reserve_expire_user_result = {
    "return": False,
    "msg": "not exists reservation",
    "data": None
}
reserve_user_result = {
    "return": True,
    "msg":"",
    "data":{
        "res_id":"22558",
        "res_ef_no":"IF025",
        "res_ur_name":"홍길동",
        "res_start_dt":"2018-12-06 12:00:00",
        "res_end_dt":"2018-12-06 15:00:00"
    }
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("device/rfid")

def on_disconnect(client, userdata, rc):
    print('c')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.split('/')
    device = payload[0]
    user = payload[1]

    device_id = DEVICES.get(device, 'Undefined')
    user_id = user[14:22]

    print(device_id)
    print(user_id)

    # if user_id:
    #     res = requests.post(api_ip, data={
    #         'ef_no': device_id,
    #         'school_num': user_id,
    #     })

    #     if res.status_code == 200:
    #         # result = res.json()

    #         # t = '2018-12-06 14:20:00'
    #         # tmp = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    #         # if (tmp > datetime.now()):
    #         #     result = reserve_user_result
    #         # else:
    #         #     result = reserve_expire_user_result

    #         result = auth_user_result

    #         if result.get('return'):
    #             data = result.get('data')

    #             if data.get('res_start_dt') is None:
    #                 # 라이센스가 있는 유저
    #                 isSuccess = True
    #             else:
    #                 # 예약한 유저
    #                 start = datetime.strptime(data.get('res_start_dt'), '%Y-%m-%d %H:%M:%S')
    #                 end = datetime.strptime(data.get('res_end_dt'), '%Y-%m-%d %H:%M:%S')

    #                 if datetime.now() > start and datetime.now() < end:
    #                     d, _ = Device.objects.get_or_create(
    #                         device_id=device_id
    #                     )
    #                     d.user_id = user_id
    #                     d.is_active = True
    #                     d.expired = end
    #                     d.save()

    #                     isSuccess = True
            
    # if isSuccess:
    #     message = "1"
    # else:
    #     message = "0"
        
    # mqttc.publish("device", "{}{}".format(device, message))


def on_subscribe(client, userdata, mid, granted_qos):
    print(client, userdata)

def on_publish(client, userdata, mid):
    print('b')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()