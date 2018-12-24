from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from django.views.generic import TemplateView
import paho.mqtt.client as mqtt
import requests
from config.mqtt import client as mqttc
from .models import Device
from apps.device.devices import DEVICES, UNREGISTER


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
        "res_start_dt":"2018-12-12 10:00:00",
        "res_end_dt":"2018-12-12 11:50:00"
    }
}


class DeviceView(APIView):
    parser_classes = [FormParser]

    def post(self, request, *args, **kwargs):
        user = request.data.get('value')
        device = request.data.get('dId')
        isSuccess = False
        device_id = DEVICES.get(device, 'Undefined')

        # if device in UNREGISTER:
        #     mqttc.publish("device", "{}1".format(device))
        # else:
        if len(user) > 0:
            user_id = user[14:22]
            res = requests.post(api_ip, data={
                'ef_no': device_id,
                'school_num': user_id,
            })

            if res.status_code == 200:
                result = res.json()

                # t = '2018-12-12 11:50:00'
                # tmp = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                # if (tmp > datetime.now()):
                #     result = reserve_user_result
                # else:
                #     result = reserve_expire_user_result

                result = auth_user_result

                # print(result)

                if result.get('return'):
                    data = result.get('data')

                    if data.get('res_start_dt') is None:
                        # 라이센스가 있는 유저
                        isSuccess = True
                    else:
                        # 예약한 유저
                        start = datetime.strptime(data.get('res_start_dt'), '%Y-%m-%d %H:%M:%S')
                        end = datetime.strptime(data.get('res_end_dt'), '%Y-%m-%d %H:%M:%S')

                        if datetime.now() > start and datetime.now() < end:
                            d, _ = Device.objects.get_or_create(
                                device_id=device_id
                            )
                            d.user_id = user_id
                            d.is_active = True
                            d.expired = end
                            d.save()

                            isSuccess= True
            
        if isSuccess:
            message = "1"
        else:
            message = "0"
            
        mqttc.publish("device", "{}{}".format(device, message))
 
        return Response()