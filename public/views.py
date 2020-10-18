import logging

from django.conf import settings
from django.http import HttpResponse
from django.template import loader


log = logging.getLogger(__name__)

def index(request):
	template = loader.get_template('index.html')
	context = {
		'user': request.user,
		'DEMO_MODE': settings.DEMO_MODE,
	}
	return HttpResponse(template.render(context, request))
