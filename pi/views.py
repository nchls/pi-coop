import os, re

from decimal import Decimal
from django.http import HttpResponse, JsonResponse



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
	with open('/var/log/coop/coop.log') as fl:
		lines = fl.readlines()
	return JsonResponse({
		'entries': lines[-30:]
	})


def get_temperature():
	temperature_raw = os.popen('vcgencmd measure_temp').readline()
	temperature_celsius = Decimal(re.sub('[^0-9\.]', '', temperature_raw))
	temperature_fahrenheit = (Decimal(temperature_celsius) * 9/5) + 32
	return (temperature_fahrenheit, temperature_celsius)


def get_uptime():
	uptime = os.popen('uptime -p').readline().replace('\n', '')
	return uptime


def get_memory_usage():
	memory_percent = os.popen('free -t | awk \'NR == 2 {print $3/$2*100}\'').readline().replace('\n', '')
	swap_percent = os.popen('free -t | awk \'NR == 3 {print $3/$2*100}\'').readline().replace('\n', '')
	return (memory_percent, swap_percent)


def get_load_averages():
	load_averages_raw = os.popen("uptime  | grep -o '[0-9]\+\.[0-9]\+*'").readlines()
	load_averages = [float(re.sub('[^0-9\.]', '', average_raw)) for average_raw in load_averages_raw]
	return load_averages
