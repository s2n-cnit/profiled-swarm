import importlib
import signal
import sys
from typing import Any, Iterable, Self, Type

from log import Error, logger
from packets import Kind


def is_iter(target: Any) -> bool:
    return hasattr("__iter__")


def make_iter(target: Any) -> Iterable:
    if is_iter(target):
        return list(target)
    return target


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
    __required_fields = {
        "ip_source": make_iter,
        "ip_dest": make_iter,
        "count": make_iter,
        "interval": make_iter,
        "kind": str,
        "duration_seconds": int,
    }

    __optional_fields = {"test": False, "show": False}

    @staticmethod
    def validate(cls: Type[Self]):
        for f, v in Profile.__required_fields.items():
            if not hasattr(cls, f):
                logger.error(f"Profile {cls.__name__} not define field {f}")
                sys.exit(Error.NOT_FIELD_PROFILE)
            setattr(cls, f, make_iter(getattr(cls, f)))
        for f, v in Profile.__optional_fields.items():
            if not hasattr(cls, f):
                setattr(cls, f, v)
        if not hasattr(Kind, cls.kind.upper()):
            logger.error(f"Kind {cls.kind} not valid")
            sys.exit(Error.NOT_VALID_KIND)
        if cls.duration_seconds > 0:
            logger.info(
                f"Set duration of generation: {cls.duration_seconds} seconds"
            )
            signal.signal(signal.SIGALRM, duration_end)
            signal.alarm(cls.duration_seconds)
        if len(cls.interval) != len(cls.count):
            logger.error(
                f"Profile {cls.__name__} has internal and count"
                "fields not of the same length"
            )
            sys.exit(Error.NOT_VALID_FIELD)
