from solo.admin import SingletonModelAdmin
from django.contrib import admin

from .models import Config


admin.site.register(Config, SingletonModelAdmin)
