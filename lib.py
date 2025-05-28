import importlib
import sys
from typing import Any, Iterable

from log import Error, logger


def is_iter(target: Any) -> bool:
    return hasattr(target, "__iter__")


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
