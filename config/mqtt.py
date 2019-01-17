from datetime import datetime
import requests
import paho.mqtt.client as mqtt

from apps.device.devices import DEVICES

api_ip = 'https://ideafactory.kaist.ac.kr/api/getReservationForTag'
auth_user_result = {
    "return": True,
    "msg": "nonbooking eqipment",
    "data": {
        "res_id": None,
        "res_ef_no": "IF025",
        "res_ur_name": "홍길동",
        "res_start_dt": None,
        "res_end_dt": None
    }
}


def on_connect(client, userdata, flags, rc):
    client.subscribe("device/rfid")


def on_message(client, userdata, msg):
    # print("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload))
    # payload = msg.payload.decode('utf-8')
    payload = msg.payload
    p = payload.decode('cp949')

    data = p.split('/')
    device = data[0]
    user = data[1]
    isSuccess = False

    device_id = DEVICES.get(device, 'Undefined')
    user_id = user[14:22]

    print(device_id, user_id)

    if user_id:
        res = requests.post(api_ip, data={
            'ef_no': device_id,
            'school_num': user_id,
        })

        if res.status_code == 200:
            result = auth_user_result

            if result.get('return'):
                data = result.get('data')

                if data.get('res_start_dt') is None:
                    # 라이센스가 있는 유저
                    isSuccess = True
                else:
                    # 예약한 유저
                    pass
                    # start = datetime.strptime(data.get('res_start_dt'), '%Y-%m-%d %H:%M:%S')
                    # end = datetime.strptime(data.get('res_end_dt'), '%Y-%m-%d %H:%M:%S')

                    # if datetime.now() > start and datetime.now() < end:
                    #     d, _ = Device.objects.get_or_create(
                    #         device_id=device_id
                    #     )
                    #     d.user_id = user_id
                    #     d.is_active = True
                    #     d.expired = end
                    #     d.save()

                    #     isSuccess = True
    
    if isSuccess:
        message = "1"
    else:
        message = "0"

    try:
        client.publish("device", "{}{}".format(device, message))
        
    except Exception as e:
        print(e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mosquitto", 1883, 60)
# client.connect("localhost", 1883, 60)