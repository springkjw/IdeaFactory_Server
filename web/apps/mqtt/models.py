from django.db import models


class Mqtt(models.Model):
    msg = models.TextField(
        verbose_name='메세지'
    )
    topic = models.CharField(
        max_length=180,
        default="",
        verbose_name='토픽'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='시간'
    )

    class Meta:
        db_table = 'mqtt'
        verbose_name = 'MQTT'
        verbose_name_plural = 'MQTT'

    def __str__(self):
        return self.msg


class Device(models.Model):
    card_id = models.CharField(
        max_length=150,
        verbose_name='카드 ID'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='활성화 여부'
    )
    timestamp = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'device'
