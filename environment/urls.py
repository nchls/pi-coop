from django.urls import path

from . import views

urlpatterns = [
    path('logs', views.log_entries, name='log_entries'),
]
