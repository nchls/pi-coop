import django
import logging
import RPi.GPIO as gpio
import time

from datetime import datetime, timedelta, timezone
from django.conf import settings
from skyfield import almanac, api
try:
	# This will work when the functions are imported from a Django module, but not when the script is run
	from door.models import Config, State, Fault
except django.core.exceptions.AppRegistryNotReady:
	pass

log = logging.getLogger(__name__)

PIN_HALL_SENSOR_UPPER = 19
PIN_HALL_SENSOR_LOWER = 20
PIN_MOTOR_LOGIC = 27
PIN_MOTOR_INPUT_1 = 6
PIN_MOTOR_INPUT_2 = 22

SENSOR_RESOLUTION_SECONDS = 0.2
MAX_DOOR_OPENING_SECONDS = 60
DELTA_FROM_SUNRISE = timedelta(hours=1)
DELTA_FROM_SUNSET = timedelta(minutes=30)


def setup_gpio():
	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_HALL_SENSOR_UPPER, gpio.IN, pull_up_down=gpio.PUD_UP)
	gpio.setup(PIN_HALL_SENSOR_LOWER, gpio.IN, pull_up_down=gpio.PUD_UP)
	gpio.setup(PIN_MOTOR_LOGIC, gpio.OUT)
	gpio.setup(PIN_MOTOR_INPUT_1, gpio.OUT)
	gpio.setup(PIN_MOTOR_INPUT_2, gpio.OUT)


def uses_gpio(fn):
	def wrapper(*args, **kwargs):
		if __name__ == '__main__':
			return fn(*args, **kwargs)
		setup_gpio()
		try:
			return fn(*args, **kwargs)
		except Exception as exc:
			log.exception(exc)
		finally:
			gpio.cleanup()
	return wrapper


def job():
	if is_daytime():
		if is_door_closed():
			open_door()
	else:
		if is_door_open():
			close_door()


def open_door():
	if is_door_open():
		log.error('Door is already open')
		return False
	set_motor_clockwise()
	start_time = time.perf_counter()
	while True:
		time.sleep(SENSOR_RESOLUTION_SECONDS)
		if is_door_open():
			turn_off_motor()
			return True
		if (time.perf_counter() - start_time) > MAX_DOOR_OPENING_SECONDS:
			turn_off_motor()
			log.error('Door did not open in time! Something is wrong...')
			return False


def close_door():
	if is_door_closed():
		log.error('Door is already closed')
		return False
	set_motor_counterclockwise()
	start_time = time.perf_counter()
	while True:
		time.sleep(SENSOR_RESOLUTION_SECONDS)
		if is_door_closed():
			turn_off_motor()
			return True
		if (time.perf_counter() - start_time) > MAX_DOOR_OPENING_SECONDS:
			turn_off_motor()
			log.error('Door did not close in time! Something is wrong...')
			return False


@uses_gpio
def set_motor_clockwise():
	gpio.output(PIN_MOTOR_LOGIC, gpio.HIGH)
	gpio.output(PIN_MOTOR_INPUT_1, gpio.HIGH)
	gpio.output(PIN_MOTOR_INPUT_2, gpio.LOW)


@uses_gpio
def set_motor_counterclockwise():
	gpio.output(PIN_MOTOR_LOGIC, gpio.HIGH)
	gpio.output(PIN_MOTOR_INPUT_1, gpio.LOW)
	gpio.output(PIN_MOTOR_INPUT_2, gpio.HIGH)


@uses_gpio
def turn_off_motor():
	gpio.output(PIN_MOTOR_LOGIC, gpio.LOW)
	gpio.output(PIN_MOTOR_INPUT_1, gpio.LOW)
	gpio.output(PIN_MOTOR_INPUT_2, gpio.LOW)


def is_door_open():
	return (is_magnet_at_upper_sensor() and not is_magnet_at_lower_sensor())


def is_door_closed():
	return (is_magnet_at_lower_sensor() and not is_magnet_at_upper_sensor())


@uses_gpio
def is_magnet_at_upper_sensor():
	return (gpio.input(PIN_HALL_SENSOR_UPPER) == 0)


@uses_gpio
def is_magnet_at_lower_sensor():
	return (gpio.input(PIN_HALL_SENSOR_LOWER) == 0)


def is_daytime():
	pownal = api.Topos('43.921554 N', '70.147969 W')
	ts = api.load.timescale(builtin=True)
	eph = api.load_file('/home/pi/skyfield-data/de421.bsp')
	now = datetime.now().astimezone()
	today_start = datetime(now.year, now.month, now.day).astimezone()
	today_end = today_start + timedelta(days=1)
	today_start_ts = ts.utc(today_start)
	today_end_ts = ts.utc(today_end)
	traversals, is_sunrise = almanac.find_discrete(today_start_ts, today_end_ts, almanac.sunrise_sunset(eph, pownal))
	# If there are multiple sunrises in a day then we have bigger problems than opening the coop door at the right time
	sunrise_iso = traversals[0].utc_iso() if is_sunrise[0] else traversals[1]
	sunset_iso = traversals[1].utc_iso() if not is_sunrise[1] else traversals[0]
	sunrise_dtm = datetime.strptime(sunrise_iso, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) + DELTA_FROM_SUNRISE
	sunset_dtm = datetime.strptime(sunset_iso, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) + DELTA_FROM_SUNSET
	return sunrise_dtm < now < sunset_dtm


if __name__ == '__main__':
	setup_gpio()
	try:
		django.setup()
		from door.models import Config, State, Fault
		job()
	except Exception as exc:
		log.exception(exc)
	finally:
		gpio.cleanup()

