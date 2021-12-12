import bme680
import django
import logging
import time

from datetime import datetime, timedelta
from django.conf import settings
try:
	# This will work when the functions are imported from a Django module, but not when the script is run
	from environment.models import Config, LogEntry
except (django.core.exceptions.AppRegistryNotReady, ModuleNotFoundError):
	pass

log = logging.getLogger(__name__)


def job():
	cfg = Config.objects.get()
	if cfg.is_environment_logging_enabled is False:
		return False
	return log_environment()


def log_environment():
	sensor = bme680.BME680()

	sensor.set_humidity_oversample(bme680.OS_2X)
	sensor.set_pressure_oversample(bme680.OS_4X)
	sensor.set_temperature_oversample(bme680.OS_8X)
	sensor.set_filter(bme680.FILTER_SIZE_3)

	start_time = time.perf_counter()
	while True:
		if sensor.get_sensor_data():
			temperature = (sensor.data.temperature * (9/5)) + 32
			LogEntry.objects.create(type=LogEntry.TEMPERATURE, value=temperature)
			pressure = sensor.data.pressure
			LogEntry.objects.create(type=LogEntry.PRESSURE, value=pressure)
			humidity = sensor.data.humidity
			LogEntry.objects.create(type=LogEntry.HUMIDITY, value=humidity)
			break

		elapsed_time = time.perf_counter() - start_time
		if elapsed_time > 30:
			log.warning('Unable to get sensor data after 30 seconds')
			return False

		time.sleep(1)

	return True


if __name__ == '__main__':
	django.setup()
	from environment.models import Config, LogEntry
	try:
		job()
	except Exception as exc:
		log.exception(exc)
