import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')

BIGINT_MAX_VALUE = sys.maxsize
BIGINT_MIN_VALUE = -1 * sys.maxsize - 1
LOG_LEVEL = 'DEBUG'

# DB SECTION
DB_CONNECTION = 'postgresql+psycopg2://billing:billing@db/billing'
# DB_CONNECTION = 'postgresql+psycopg2://billing:billing@localhost:6432/billing'
TESTING_DB_CONNECTION = 'postgresql+psycopg2://billing:billing@localhost:6433/billing'
DB_CONNECTION_YOYO = DB_CONNECTION.replace('+psycopg2', '')

# REDIS SECTION
# REDIS_CONNECTION = 'redis://localhost:6379/0'
REDIS_CONNECTION = 'redis://redis'
REDIS_CACHE_DEFAULT_TIMEOUT = 60  # 60 seconds (1 min)

# AMQP SECTION

AMQPS = {}


# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['debug_file'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'stream': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'debug_file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'error.log'),
        },
        'access_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'access.log'),
        }
    },
    'loggers': {
        'worker': {
            'level': LOG_LEVEL,
            'handlers': ['stream'],
        },
        'billing': {
            'level': LOG_LEVEL,
            'handlers': ['error_file', 'debug_file'],
            'propagate': False,
        },
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['error_file'],
            'propagate': True,
        },
        'uvicorn.access': {
            'level': 'INFO',
            'handlers': ['access_file'],
            'propagate': False,
        },
    },
}