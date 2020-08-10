from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('status', views.status, name='status'),
    path('open', views.open_door, name='open'),
    path('close', views.close_door, name='close'),
    path('up', views.motor_up, name='up'),
    path('down', views.motor_down, name='down'),
    path('off', views.motor_off, name='off'),
]

