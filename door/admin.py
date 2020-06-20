from django.contrib import admin

from .models import Config, State, Fault

admin.site.register(Config)
admin.site.register(State)
admin.site.register(Fault)

