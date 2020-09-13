from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

def favicon(request):
	return redirect(to='/static/images/favicon-16x16.png')

urlpatterns = [
	path('', include('public.urls')),
	path('door/', include('door.urls')),
	path('pi/', include('pi.urls')),
	path('admin/', admin.site.urls),
	path('favicon.ico', favicon),
]
