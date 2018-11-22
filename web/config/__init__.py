from . import mqtt
from .tasks import app as celery_app

mqtt.client.loop_start()
 
__all__ = ['celery_app']
