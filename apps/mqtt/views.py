from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from django.views.generic import TemplateView
import paho.mqtt.client as mqtt
import requests
from config.mqtt import client as mqttc
from .models import Device

topics = {
    'DEVICE_STATUS': 'device',
}
# DEVICE_STATUS 1 : 장비 켜짐 / 0 : 장비 꺼짐

devices = {
    '2C:3A:E8:43:BB:4C': 'IF001',
    'B4:E6:2D:3E:91:71': 'IF010',
}

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
    "return": True,
    "msg":"",
    "data":{
        "res_id":"22558",
        "res_ef_no":"IF025",
        "res_ur_name":"홍길동",
        "res_start_dt":"2018-11-01 13:30:00",
        "res_end_dt":"2018-11-01 16:00:00"
    }
}
reserve_user_result = {
    "return": True,
    "msg":"",
    "data":{
        "res_id":"22558",
        "res_ef_no":"IF025",
        "res_ur_name":"홍길동",
        "res_start_dt":"2018-11-28 06:00:00",
        "res_end_dt":"2018-11-28 18:30:00"
    }
}


class DeviceView(APIView):
    parser_classes = [FormParser]

    def post(self, request, *args, **kwargs):
        # try:
        user = request.data.get('value')
        device = request.data.get('dId')
        
        user_id = user[14:22]
        device_id = devices.get(device, 'Undefined')

        d, _ = Device.objects.get_or_create(
            device_id=device_id
        )

        if user_id is not None and user_id != '':
            if not d.is_active:
                # 예약 사이트에 요청
                res = requests.post(api_ip, data={
                    'ef_no': device_id,
                    'school_num': user_id,
                })
                # if res.status_code == 200:
                if res.status_code == 404:
                    # result = res.json()
                    result = reserve_user_result
                    
                    if result.get('return'):
                        data = result.get('data')

                        if data.get('res_start_dt') is None:
                            d.is_active = True
                            d.save()
                            mqttc.publish(device, "1")
                        else:
                            start = datetime.strptime(data.get('res_start_dt'), '%Y-%m-%d %H:%M:%S')
                            end = datetime.strptime(data.get('res_end_dt'), '%Y-%m-%d %H:%M:%S')

                            if datetime.now() > start and datetime.now() < end:
                                d.is_active = True
                                d.save()
                                mqttc.publish(device, "1")
        else:
            if d.is_active:
                d.is_active = False
                d.save()

                mqttc.publish(device, "0")
        return Response()