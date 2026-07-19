"""
WSGI config for coop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import site
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

try:
	for package_path in site.getsitepackages():
		sys.path.append(package_path)
except AttributeError:
	sys.path.append(site.getusersitepackages())

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coop.settings')

application = get_wsgi_application()
