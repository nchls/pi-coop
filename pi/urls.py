from django.urls import path

from . import views

urlpatterns = [
    path('status', views.get_pi_status, name='pi_status'),
]

