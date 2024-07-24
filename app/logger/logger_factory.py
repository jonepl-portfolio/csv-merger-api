import os
import logging
import logging.config
from enum import Enum
from logging import Logger

from dotenv import load_dotenv

import logger.config.config as config
from logger.config.constants import (
    ROOT_LOGGER_NAME,
    FILE_HANDLER_KEY,
    FILENAME_KEY,
    HANDLERS_KEY,
)

load_dotenv()


class AppEnv(Enum):
    DEV = "DEV"
    PROD = "PROD"
    STAGING = "STAGING"
    TEST = "TEST"


env = os.environ.get("APP_ENV")

if env == AppEnv.DEV.value:
    config = config.dev_config
elif env == AppEnv.PROD.value:
    config = config.prod_config
elif env == AppEnv.TEST.value:
    config = config.test_config
elif env == AppEnv.STAGING.value:
    config = config.prod_config
else:
    config = config.dev_config

dirName = os.path.dirname(
    config.get(HANDLERS_KEY).get(FILE_HANDLER_KEY).get(FILENAME_KEY)
)
os.makedirs(dirName, exist_ok=True)

logging.config.dictConfig(config)


class LoggerFactory(object):
    """
    DEBUG: Purpose: Used for detailed information, typically of interest only when diagnosing problems
    INFO: Purpose: Used to confirm that things are working as expected.
    WARN: Used to indicate potential problems that are not necessarily errors, but may require attention.
    ERROR: Used to indicate more serious problems that need to be addressed.
    CRITICAL: Used for very serious errors that indicate a failure in a critical part of the application.
    """

    _LOG = None

    @classmethod
    def _initialize(cls):
        if cls._LOG is None:
            cls._LOG = logging.getLogger(ROOT_LOGGER_NAME)

    @staticmethod
    def get_root_logger():
        return LoggerFactory._LOG

    @staticmethod
    def get_logger(moduleName: str) -> Logger:
        """
        A static method called by other modules to initialize logger in
        their own module.
        """
        LoggerFactory._initialize()
        return LoggerFactory._LOG.getChild(moduleName)
