from django.contrib import admin

from .models import Device

class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'is_active',
        'expired',
    ]

admin.site.register(Device, DeviceAdmin)