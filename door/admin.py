from solo.admin import SingletonModelAdmin
from django.contrib import admin

from .models import Config, State, Fault


class FaultAdmin(admin.ModelAdmin):
	list_display = ['message', 'created', 'is_resolved']

admin.site.register(Config, SingletonModelAdmin)
admin.site.register(State, SingletonModelAdmin)
admin.site.register(Fault, FaultAdmin)

