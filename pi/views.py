import locale, os, re

from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.conf import settings


try:
	locale.setlocale(locale.LC_ALL, 'USA')
except Exception:
	pass

def get_pi_status(request):
	temperature_fahrenheit, temperature_celsius = get_temperature()
	uptime = get_uptime()
	memory_percent, swap_percent = get_memory_usage()
	load_averages = get_load_averages()
	return JsonResponse({
		'temperatureCelsius': round(float(temperature_celsius)),
		'temperatureFahrenheit': round(float(temperature_fahrenheit)),
		'uptime': uptime,
		'memoryPercent': round(float(memory_percent)),
		'swapPercent': round(float(swap_percent)),
		'loadAverages': load_averages,
	})


def get_log(request):
	with open(settings.LOG_FILE) as fl:
		lines = fl.readlines()
	return JsonResponse({
		'entries': lines[-30:]
	})


def get_temperature():
	if settings.DEMO_MODE:
		return (Decimal('100'), Decimal('100'))
	temperature_raw = os.popen('vcgencmd measure_temp').readline()
	temperature_celsius = Decimal(re.sub('[^0-9\.]', '', temperature_raw))
	temperature_fahrenheit = (Decimal(temperature_celsius) * 9/5) + 32
	return (temperature_fahrenheit, temperature_celsius)


def get_uptime():
	if settings.DEMO_MODE:
		return '3 hours'
	uptime = os.popen('uptime -p').readline().replace('\n', '')
	return uptime


def get_memory_usage():
	if settings.DEMO_MODE:
		return ('4', '0')
	memory_percent = os.popen('free -t | awk \'NR == 2 {print $3/$2*100}\'').readline().replace('\n', '')
	swap_percent = os.popen('free -t | awk \'NR == 3 {print $3/$2*100}\'').readline().replace('\n', '')
	return (memory_percent, swap_percent)


def get_load_averages():
	if settings.DEMO_MODE:
		return '0.22,0.1,0.02'
	load_averages_raw = os.popen("uptime  | grep -o '[0-9]\+\.[0-9]\+*'").readlines()
	load_averages = [float(re.sub('[^0-9\.]', '', average_raw)) for average_raw in load_averages_raw]
	return load_averages
