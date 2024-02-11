import os

SECRET_KEY = 'secret secrets'

ALERT_EMAIL_ADDRESSES = (
	'ian@nchls.com',
)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = 'coopalerts@gmail.com'
GMAIL_PASSWORD = 'hunter2'

DEMO_MODE = True

DEBUG = True

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'simple': {
			'format': '[{levelname}] - {message}',
			'style': '{',
		},
		'verbose': {
			'format': '{asctime} [{levelname}] ({filename}:{funcName}) - {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'simple',
		},
		'file': {
			'level': 'INFO',
			'class': 'logging.FileHandler',
			'filename': '/dev/pi-coop/coop.log',
			'formatter': 'verbose',
		},
		'email': {
			'level': 'ERROR',
			'class': 'coop.alerts.EmailAlertHandler',
		},
	},
	'root': {
		'handlers': [
			'console',
			'file',
		],
		'level': 'INFO',
	},
}

STATIC_ROOT = ''
STATICFILES_DIRS = (os.path.join('/', 'dev', 'pi-coop', 'static'),)

SKYFIELD_DATA_PATH = os.path.join('/', 'dev', 'pi-coop', 'de421.bsp')
