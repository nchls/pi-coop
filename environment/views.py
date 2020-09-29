import logging

from datetime import datetime, timedelta, timezone
from django.http import HttpResponse, JsonResponse

from environment.models import Config, LogEntry


log = logging.getLogger(__name__)

def log_entries(request):
	cfg = Config.get_solo()

	start_time = datetime.now() + timedelta(days=-5)

	temp_entries = LogEntry.objects.filter(
		type=LogEntry.TEMPERATURE,
		created__gte=start_time
	).order_by('created')
	pres_entries = LogEntry.objects.filter(
		type=LogEntry.PRESSURE,
		created__gte=start_time
	).order_by('created')
	humd_entries = LogEntry.objects.filter(
		type=LogEntry.HUMIDITY,
		created__gte=start_time
	).order_by('created')

	return JsonResponse({
		'isEnvironmentLoggingEnabled': cfg.is_environment_logging_enabled,
		'logEntries': {
			'temperature': list(
				(e.created.replace(tzinfo=timezone.utc).astimezone(), e.value) for e in temp_entries
			),
			'pressure': list(
				(e.created.replace(tzinfo=timezone.utc).astimezone(), e.value) for e in pres_entries
			),
			'humidity': list(
				(e.created.replace(tzinfo=timezone.utc).astimezone(), e.value) for e in humd_entries
			),
		},
	})
