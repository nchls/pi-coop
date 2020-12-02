import logging

from django.conf import settings
from twilio.rest import Client

class TextMessageAlertHandler(logging.Handler):
	def emit(self, record):
		if not settings.DEMO_MODE:
			account_sid = settings.TWILIO_ACCOUNT_SID
			auth_token = settings.TWILIO_AUTH_TOKEN
			client = Client(account_sid, auth_token)
			for num in settings.ALERT_PHONE_NUMBERS:
				try:
					message = client.messages.create(
						body=f'Chicken coop alert: {record.getMessage()}',
						from_='+12105985068',
						to=num
					)
				except:
					pass
