import logging

from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse

from door.models import Config
from door.tasks import (
	is_door_open, 
	is_door_closed, 
	open_door, 
	close_door,
	set_motor_clockwise,
	set_motor_counterclockwise,
	turn_off_motor,
	get_sunrise_sunset_times,
	DELTA_FROM_SUNSET
)


log = logging.getLogger(__name__)

def index(request):
	return HttpResponse('Door?')

def status(request):
	if is_door_open():
		door_status = 'OPEN'
	elif is_door_closed():
		door_status = 'CLOSED'
	else:
		door_status = 'INDETERMINATE'

	cfg = Config.get_solo()

	_, sunset_dtm = get_sunrise_sunset_times()
	closing_time = sunset_dtm + DELTA_FROM_SUNSET + timedelta(minutes=1)

	return JsonResponse({
		'doorStatus': door_status,
		'isAutoOpenCloseEnabled': cfg.is_auto_open_close_enabled,
		'closingTime': closing_time.strftime('%-I:%M'),
	})

@staff_member_required
def open_door(request):
	open_door()
	return JsonResponse({
		'success': True,
	})

@staff_member_required
def close_door(request):
	close_door()
	return JsonResponse({
		'success': True,
	})

@staff_member_required
def motor_up(request):
	set_motor_counterclockwise()
	return JsonResponse({
		'success': True,
	})

@staff_member_required
def motor_down(request):
	set_motor_clockwise()
	return JsonResponse({
		'success': True,
	})

@staff_member_required
def motor_off(request):
	turn_off_motor()
	return JsonResponse({
		'success': True,
	})


