import logging
import logging.config
import os
import pdb

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

DEBUG = 'debug'
ERROR = 'error'
INFO = 'info'
WARNING = 'warning'
LOG_LEVEL_ENV = 'MSM_SCHEDULER_LOG_LEVEL'

class Logger:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, name = None):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        cls._instance.load()

        if not name:
            return logging
        else:
            return logging.getLogger(name)

    @classmethod
    def reload(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        cls._instance.load()

    def load(self):
        log_level = os.getenv(LOG_LEVEL_ENV) or ''

        if log_level.lower() == DEBUG:
            logging.config.dictConfig({'disable_existing_loggers': True, 'version': 1})
            logging.basicConfig(level=logging.DEBUG)
        elif log_level.lower() == WARNING:
            logging.basicConfig(level=logging.WARNING)
        elif log_level.lower() == ERROR:
            logging.basicConfig(level=logging.ERROR)
        else:
            logging.basicConfig(level=logging.INFO)