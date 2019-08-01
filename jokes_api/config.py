from os import environ
from logging import Filter

from flask import request
from flask_login import current_user
from dotenv import load_dotenv


load_dotenv('.env')


class DefaultConfig(object):
    """Default configuration"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('JOKES_API_DATABASE_URL')

    LOG_LEVEL = environ.get('JOKES_API_LOG_LEVEL', 'INFO')

    JOKES_PROVIDER_URL = environ.get(
        'JOKES_API_PROVIDER_URL', 'https://geek-jokes.sameerkumar.website/api')


class UserContext(Filter):
    def filter(self, record):
        record.user = str(current_user or 'anonymous')
        record.ip = request.environ.get('REMOTE_ADDR')
        return True


LoggingConfig = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'user_context': {'()': UserContext}
    },
    'formatters': {
        'default_format': {
            'style': '{',
            'format': '[{asctime}] [{levelname}] [{ip}] [{user}] {message}'
        }
    },
    'handlers': {
        'default_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_format',
            'filters': ['user_context'],
            'filename': 'audit.log'
        }
    },
    'loggers': {
        'jokes_api': {
            'level': DefaultConfig.LOG_LEVEL,
            'handlers': ['default_handler']
        }
    }
}
