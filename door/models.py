from django.db import models

class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = 'door'


class Config(BaseModel):
    is_auto_open_close_enabled = models.BooleanField(default=True)


class State(BaseModel):
    is_moving = models.BooleanField(default=False)

    
class Fault(BaseModel):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000)
    is_resolved = models.BooleanField(default=False)

