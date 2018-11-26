from django.urls import path

from . import views

urlpatterns = [
    path('device/', views.DeviceView().as_view()),
]