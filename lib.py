import importlib
import signal
import sys
from typing import Any, Self, Type

from log import Error, logger
from packets import Kind


def duration_end(signum, frame):
    logger.info("Generation done.")
    exit(0)


def load_module(path: str) -> Any:
    return importlib.import_module(path)


def load_class(path: str) -> Any:
    parts = path.split(".")
    module_path = ".".join(parts[:-1])
    module = load_module(module_path)
    klass = parts[-1]
    if not hasattr(module, klass):
        logger.error(f"Module {module_path} has not defined {klass}")
        sys.exit(Error.NOT_PROFILE)
    return getattr(module, klass)


class Profile:
    __required_fields = [
        "ip_source",
        "ip_dest",
        "count",
        "interval",
        "kind",
        "duration_seconds",
    ]

    __optional_fields = ["test", "show"]

    @staticmethod
    def validate(cls: Type[Self]):
        for f in Profile.__required_fields:
            if not hasattr(cls, f):
                logger.error(f"Profile {cls.__name__} not define field {f}")
                sys.exit(Error.NOT_FIELD_PROFILE)
        for f in Profile.__optional_fields:
            if not hasattr(cls, f):
                setattr(cls, f, False)
        if not hasattr(Kind, cls.kind.upper()):
            logger.error(f"Kind {cls.kind} not valid")
            sys.exit(Error.NOT_VALID_KIND)
        if cls.duration_seconds > 0:
            logger.info(
                f"Set duration of generation: {cls.duration_seconds} seconds"
            )
            signal.signal(signal.SIGALRM, duration_end)
            signal.alarm(cls.duration_seconds)
