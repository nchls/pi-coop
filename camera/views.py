import logging
import os

from django.http import JsonResponse


log = logging.getLogger(__name__)

def ping(request):
	os.popen('touch /home/pi/coop/camera/sentinel')
	motion_service = os.popen('systemctl is-active motion').readline()
	if not motion_service.startswith('active'):
		os.popen('service motion start')

	return JsonResponse({
		'success': True,
	})
