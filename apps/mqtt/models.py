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
    device_id = models.CharField(
        max_length=150,
        verbose_name='장비 ID'
    )
    user_id = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='사용자 ID',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='활성화 여부'
    )
    expired = models.DateTimeField(
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        db_table = 'device'

    def __str__(self):
        return self.device_id