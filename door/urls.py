from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('status', views.status, name='status'),
    path('open', views.open_door, name='open'),
    path('close', views.close_door, name='close'),
]

