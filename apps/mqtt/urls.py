from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('rfid', views.RFIDView.as_view()),
    path('<str:board>/<str:action>', views.TestView.as_view()),
]