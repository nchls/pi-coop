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
except (django.core.exceptions.AppRegistryNotReady, ModuleNotFoundError):
	pass

log = logging.getLogger(__name__)

PIN_HALL_SENSOR_UPPER = 19
PIN_HALL_SENSOR_LOWER = 20
PIN_MOTOR_LOGIC = 27
PIN_MOTOR_INPUT_1 = 6
PIN_MOTOR_INPUT_2 = 22

SENSOR_RESOLUTION_SECONDS = 0.2
MAX_DOOR_OPENING_SECONDS = 60
DELTA_FROM_SUNRISE = timedelta(minutes=1)
DELTA_FROM_SUNSET = timedelta(minutes=45)


def setup_gpio():
	gpio.setwarnings(False)
	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_HALL_SENSOR_UPPER, gpio.IN, pull_up_down=gpio.PUD_UP)
	gpio.setup(PIN_HALL_SENSOR_LOWER, gpio.IN, pull_up_down=gpio.PUD_UP)
	gpio.setup(PIN_MOTOR_LOGIC, gpio.OUT)
	gpio.setup(PIN_MOTOR_INPUT_1, gpio.OUT)
	gpio.setup(PIN_MOTOR_INPUT_2, gpio.OUT)


def uses_gpio(fn):
	def wrapper(*args, **kwargs):
		if gpio.getmode() is None:
			setup_gpio()
		return fn(*args, **kwargs)
	return wrapper


def job():
	cfg = Config.objects.get()
	if cfg.is_auto_open_close_enabled is False:
		return False
	if Fault.objects.filter(is_resolved=False).first() is not None:
		return False
	if is_door_closed() and is_daytime():
		return open_door()
	if is_door_open() and not is_daytime():
		return close_door()


def open_door():
	log.info('Opening door')
	try:
		if not is_door_closed():
			log.error('Door is not closed; cannot open!')
			return False
		set_motor_clockwise()
		start_time = time.perf_counter()
		while True:
			time.sleep(SENSOR_RESOLUTION_SECONDS)
			if (time.perf_counter() - start_time) > 4 and is_door_closed():
				msg = 'Door doesn\'t seem to be opening!'
				Fault.objects.create(message=msg)
				log.error(msg)
				turn_off_motor()
				return False
			if (time.perf_counter() - start_time) > 45:
				log.info('Completed door opening')
				turn_off_motor()
				return True
	except Exception as exc:
		Fault.objects.create(message=f'Exception opening door! {exc}')
		log.exception('Exception opening door!')
		turn_off_motor()
		return False


def close_door():
	log.info('Closing door')
	try:
		if is_door_closed():
			log.error('Door is already closed!')
			return False
		set_motor_counterclockwise()
		start_time = time.perf_counter()
		while True:
			time.sleep(SENSOR_RESOLUTION_SECONDS)
			if is_door_closed():
				log.info(f'Completed door closing in {time.perf_counter() - start_time} seconds')
				turn_off_motor()
				return True
			if (time.perf_counter() - start_time) > 55:
				msg = 'Door did not trip lower sensor after 55 seconds!'
				Fault.objects.create(message=msg)
				log.error(msg)
				turn_off_motor()
				return False
	except Exception as exc:
		Fault.objects.create(message=f'Exception closing door! {exc}')
		log.exception('Exception closing door!')
		turn_off_motor()
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
	return not is_magnet_at_lower_sensor()


def is_door_closed():
	return is_magnet_at_lower_sensor()


@uses_gpio
def is_magnet_at_upper_sensor():
	return (gpio.input(PIN_HALL_SENSOR_UPPER) == 0)


@uses_gpio
def is_magnet_at_lower_sensor():
	return (gpio.input(PIN_HALL_SENSOR_LOWER) == 0)


def is_daytime():
	now = datetime.now().astimezone()
	sunrise_dtm, sunset_dtm = get_sunrise_sunset_times()
	start = sunrise_dtm + DELTA_FROM_SUNRISE
	end = sunset_dtm + DELTA_FROM_SUNSET
	return start < now < end


def get_sunrise_sunset_times():
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
	sunrise_dtm = datetime.strptime(sunrise_iso, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).astimezone()
	sunset_dtm = datetime.strptime(sunset_iso, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).astimezone()
	return (sunrise_dtm, sunset_dtm)


if __name__ == '__main__':
	django.setup()
	from door.models import Config, State, Fault
	try:
		job()
	except Exception as exc:
		log.exception(exc)


