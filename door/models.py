from django.db import models

class Config(models.Model):
    is_auto_open_close_enabled = models.BooleanField(default=True)

class State(models.Model):
    is_moving = models.BooleanField(default=False)
    
class Fault(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000)
    is_resolved = models.BooleanField(default=False)

