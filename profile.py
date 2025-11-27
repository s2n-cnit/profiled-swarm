import signal
import sys
from typing import Self, Type

from lib import duration_end
from log import Error, logger

# RTSP:                                     TCP/554
# YouTube Live, Vimeo, LinkedIn or Twitch:  TCP/1935
# RTMP (Periscope):                         TCP/80
# RTMPS (Facebook Live or YouTube Live):    TCP/443
# RTMP LinkedIn Live:                       TCP/1936
# RTMPS to LinkedIn Live:                   TCP/2395        TCP/2396
# VidiU speed test function:                TCP/2545        TCP/2565
# Auth YouTube Live, Facebook Live
# ---| Ustream, Livestream, and Twitch:     TCP/443/HTTPs
# DNS lookups:                              UDP/53
# Web UI of the VidiU for configuration:    TCP/443/HTTPs
# Apple Bonjour:                            TCP/5353


class Profile:
    __required_fields = [
        "count",
        "interval_seconds",
        "duration_seconds",
    ]

    __required_methods = [
        "create"
    ]

    __optional_fields = {
        "test": False,
        "show": False,
        "verbose": False
    }

    @staticmethod
    def validate(cls: Type[Self]):
        for f in Profile.__required_fields:
            if not hasattr(cls, f):
                logger.error(f"Profile {cls.__name__} not define field {f}")
                sys.exit(Error.NOT_FIELD_PROFILE)
        for f in Profile.__required_methods:
            if not hasattr(cls, f) or not callable(getattr(cls, f)):
                logger.error(f"Profile {cls.__name__} not define methods {f}")
                sys.exit(Error.NOT_METHOD_PROFILE)
        for f, v in Profile.__optional_fields.items():
            if not hasattr(cls, f):
                setattr(cls, f, v)
        if cls.duration_seconds > 0:
            logger.info(
                f"Set duration of generation: {cls.duration_seconds} seconds"
            )
            signal.signal(signal.SIGALRM, duration_end)
            signal.alarm(cls.duration_seconds)
        if len(cls.interval_seconds) != len(cls.count):
            logger.error(
                f"Profile {cls.__name__} has internal and count"
                "fields not of the same length"
            )
            sys.exit(Error.NOT_VALID_FIELD)
