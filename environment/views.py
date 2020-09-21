import logging

from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse

from environment.models import Config, LogEntry


log = logging.getLogger(__name__)

def log_entries(request):
	cfg = Config.get_solo()

	one_week_ago = datetime.now() + timedelta(days=-7)

	temp_entries = LogEntry.objects.filter(
		type=LogEntry.TEMPERATURE,
		created__gte=one_week_ago
	).order_by('created')
	pres_entries = LogEntry.objects.filter(
		type=LogEntry.PRESSURE,
		created__gte=one_week_ago
	).order_by('created')
	humd_entries = LogEntry.objects.filter(
		type=LogEntry.HUMIDITY,
		created__gte=one_week_ago
	).order_by('created')

	return JsonResponse({
		'isEnvironmentLoggingEnabled': cfg.is_environment_logging_enabled,
		'logEntries': {
			'temperature': list([{'time': e.created, 'value': e.value} for e in temp_entries]),
			'pressure': list([{'time': e.created, 'value': e.value} for e in pres_entries]),
			'humidity': list([{'time': e.created, 'value': e.value} for e in humd_entries]),
		},
	})
