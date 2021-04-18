import logging
import smtplib

from django.conf import settings

log = logging.getLogger(__name__)

class EmailAlertHandler(logging.Handler):
	def emit(self, record):
		if not settings.DEMO_MODE:
			try:
				session = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
				session.ehlo()
				session.starttls()
				session.ehlo()

				session.login(settings.GMAIL_USERNAME, settings.GMAIL_PASSWORD)

				for email in settings.ALERT_EMAIL_ADDRESSES:
					headers = [
						"From: " + settings.GMAIL_USERNAME, 
						"Subject: Chicken coop alert!", 
						"To: " + email,
						"MIME-Version: 1.0", 
						"Content-Type: text/html"
					]
					headers = "\r\n".join(headers)

					session.sendmail(settings.GMAIL_USERNAME, email, headers + "\r\n\r\n" + f'Chicken coop alert: {record.getMessage()}')

					session.quit()

			except Exception as exc:
				log.warning('Failed to send alert emails!')
				log.warning(exc)
