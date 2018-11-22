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


class DeviceView(APIView):
    parser_classes = [FormParser]

    def post(self, request, *args, **kwargs):
        # try:
        value = request.data.get('value')
        device = request.data.get('dId')
        
        student_id = value[14:22]
        device_id = devices.get(device, None)

        d, _ = Device.objects.get_or_create(
            card_id=device_id
        )

        print(student_id, device_id, d.is_active)
        if student_id is not None and student_id != '':
            if not d.is_active:
                d.is_active = True
                d.save()

                mqttc.publish(topics['DEVICE_STATUS'], "1")
        else:
            if d.is_active:
                d.is_active = False
                d.save()

                mqttc.publish(topics['DEVICE_STATUS'], "0")


        # try:
        #     if device_id is not None:
        #         # 예약 사이트에 정보 확인
        #         url = "%s/%s%s" % (
        #             api_ip,
        #             device_id,
        #             student_id,
        #         )

        #         res = requests.post(api_ip, data={
        #             'ef_no': device_id,
        #             'school_num': student_id,
        #         })

        #         if res.status_code == 200:
        #             result = res.json()
                    
        #             if result.get('return'):
        #                 # MQTT 발행
        #                 data = result.get('data')
        #                 if data:
        #                     res_ef_no = data.get('res_ef_no')
        #                     res_end_dt = data.get('res_end_dt')

        #                 mqttc.publish(topics['DEVICE_STATUS'], "1")
        #             else:
        #                 msg = result.get('msg')
        #                 # 예약은 안했지만 가입한 유저인 경우 패스
        #                 if msg == 'not exists reservation':
        #                     mqttc.publish(topics['DEVICE_STATUS'], "1")
        #         else:
        #             mqttc.publish(topics['DEVICE_STATUS'], "0")
        #     else:
        #         mqttc.publish(topics['DEVICE_STATUS'], "0")
        # except:
        #     mqttc.publish(topics['DEVICE_STATUS'], "0")
        return Response()