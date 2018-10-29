# from rest_framework.views import View
# from rest_framework.generics import CreateAPIView
# from rest_framework.response import Response
from django.views.generic import TemplateView
import paho.mqtt.client as mqtt
from config.mqtt import client as mqttc

pin = {
    'name': 'GPIO 4',
    'board': 'esp8266',
    'topic': 'esp8266/4'
}


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pin.update({
            'state': False
        })
        context.update({
            'pin': pin
        })

        return context


class TestView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        board = kwargs.get('board')
        action = kwargs.get('action')
        devicePin = pin['name']

        if action == '1' and board == 'esp8266':
            mqttc.publish(pin['topic'], "1")
            pin['state'] = True

        if action == "0" and board == 'esp8266':
            mqttc.publish(pin['topic'], "0")
            pin['state'] = False

        context = super().get_context_data(**kwargs)
        context.update({
            'pin': pin
        })

        return context


class RFIDView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pin.update({
            'state': False
        })
        context.update({
            'pin': pin
        })

        mqttc.publish(pin['topic'], "1")

        return context