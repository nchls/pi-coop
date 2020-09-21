from django.db import models
from solo.models import SingletonModel



class BaseModel(models.Model):
	class Meta:
		abstract = True
		app_label = 'environment'


class Config(BaseModel, SingletonModel):
	is_environment_logging_enabled = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Environment logging configuration'


class LogEntry(BaseModel):
	TEMPERATURE = 'TEMPERATURE'
	HUMIDITY = 'HUMIDITY'
	PRESSURE = 'PRESSURE'
	VOC = 'VOC'
	ENVIRONMENT_LOG_TYPE_CHOICES = (
		(TEMPERATURE, 'Temperature',),
		(HUMIDITY, 'Humidity',),
		(PRESSURE, 'Pressure',),
		(VOC, 'Volatile Organic Compounds',),
	)

	created = models.DateTimeField(auto_now_add=True)
	type = models.CharField(choices=ENVIRONMENT_LOG_TYPE_CHOICES, max_length=30)
	value = models.DecimalField(decimal_places=2, max_digits=8)

