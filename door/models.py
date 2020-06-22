from django.db import models
from solo.models import SingletonModel

class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = 'door'


class Config(BaseModel, SingletonModel):
    is_auto_open_close_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Door configuration'


class State(BaseModel, SingletonModel):
    is_moving = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Door state'


class Fault(BaseModel):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000)
    is_resolved = models.BooleanField(default=False)

