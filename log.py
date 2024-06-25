import sys
from enum import Enum

from loguru import logger

SEP = ", "

logger_fmt = (
    "<cyan>{time:YYYY-MM-DD HH:mm:ss.SSS}</cyan> "
    "<level>{level: <10}</level> "
    "<white>{message}</white>"
)
config = {
    "handlers": [
        {"sink": sys.stderr, "format": logger_fmt},
    ],
}
logger.configure(**config)


class Error(int, Enum):
    NOT_PROFILE = 1
    NOT_FIELD_PROFILE = 2
    NOT_VALID_KIND = 3
    NOT_VALID_FIELD = 4
