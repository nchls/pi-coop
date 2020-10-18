import logging

from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from door.models import Config, Fault
from door.tasks import (
	is_door_open, 
	is_door_closed, 
	open_door, 
	close_door,
	set_motor_clockwise,
	set_motor_counterclockwise,
	turn_off_motor,
	get_sunrise_sunset_times,
	DELTA_FROM_SUNRISE,
	DELTA_FROM_SUNSET
)


log = logging.getLogger(__name__)

def index(request):
	return HttpResponse('Door?')

def status(request):
	if settings.DEMO_MODE:
		return JsonResponse({
			'doorStatus': 'OPEN',
			'isAutoOpenCloseEnabled': True,
			'openingTime': '6:59',
			'closingTime': '6:37',
			'unresolvedFaults': [],
		})
	
	if is_door_open():
		door_status = 'OPEN'
	elif is_door_closed():
		door_status = 'CLOSED'
	else:
		door_status = 'INDETERMINATE'

	cfg = Config.get_solo()

	if request.user.is_staff:
		unresolved_faults = Fault.objects.filter(is_resolved=False)
	else:
		unresolved_faults = []

	sunrise_dtm, sunset_dtm = get_sunrise_sunset_times()
	opening_time = sunrise_dtm + DELTA_FROM_SUNRISE
	closing_time = sunset_dtm + DELTA_FROM_SUNSET

	return JsonResponse({
		'doorStatus': door_status,
		'isAutoOpenCloseEnabled': cfg.is_auto_open_close_enabled,
		'openingTime': opening_time.strftime('%-I:%M'),
		'closingTime': closing_time.strftime('%-I:%M'),
		'unresolvedFaults': list((fault.id, fault.created.astimezone(), fault.message) for fault in unresolved_faults),
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
	set_motor_clockwise()
	return JsonResponse({
		'success': True,
	})

@staff_member_required
def motor_down(request):
	set_motor_counterclockwise()
	return JsonResponse({
		'success': True,
	})

@staff_member_required
def motor_off(request):
	turn_off_motor()
	return JsonResponse({
		'success': True,
	})

@staff_member_required
@csrf_exempt
@require_POST
def resolve_fault(request, id):
	try:
		fault = Fault.objects.get(id=id)
	except ObjectDoesNotExist:
		log.warning(f'Attempted to resolve nonexistent fault (id {id})')
		return HttpResponseBadRequest()
	fault.is_resolved = True
	fault.save()
	log.info(f'Resolved fault {id}')
	return JsonResponse({
		'success': True,
	})
