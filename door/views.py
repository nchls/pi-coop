from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from door.models import Config
from door.tasks import is_door_open, is_door_closed, open_door, close_door


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

	return JsonResponse({
		'doorStatus': door_status,
		'isAutoOpenCloseEnabled': cfg.is_auto_open_close_enabled,
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
