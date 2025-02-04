"""logging settings"""

from logging import Logger, getLogger
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(pathname)s:%(lineno)d %(asctime)-15s [ %("
                "levelname)s ] : %(message)s",
            },
            "access": {
                "format": "%(pathname)s:%(lineno)d %(asctime)-15s [ %("
                "levelname)s ] : %(message)s",
            },
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "level": 10,
                "stream": "ext://sys.stdout",
            },
        },
        "root": {"level": 10, "handlers": ["console"]},
    },
)

logger: Logger = getLogger("backend logger.")
