import logging

from django.http import HttpResponse
from django.template import loader


log = logging.getLogger(__name__)

def index(request):
	template = loader.get_template('index.html')
	context = {
		'user': request.user,
	}
	return HttpResponse(template.render(context, request))
