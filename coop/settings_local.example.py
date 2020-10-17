import os

SECRET_KEY = 'secret secrets'

ALERT_PHONE_NUMBERS = ()

TWILIO_ACCOUNT_SID = 'foo'
TWILIO_AUTH_TOKEN = 'bar'

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
		'sms': {
			'level': 'ERROR',
			'class': 'coop.alerts.TextMessageAlertHandler',
		},
	},
	'root': {
		'handlers': [
			'console',
			'file',
			'sms',
		],
		'level': 'INFO',
	},
}

STATIC_ROOT = ''
STATICFILES_DIRS = (os.path.join('/', 'dev', 'pi-coop', 'static'),)

SKYFIELD_DATA_PATH = os.path.join('/', 'dev', 'pi-coop', 'de421.bsp')
