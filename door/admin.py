from solo.admin import SingletonModelAdmin
from django.contrib import admin

from .models import Config, Fault


admin.site.register(Config, SingletonModelAdmin)
admin.site.register(Fault)

