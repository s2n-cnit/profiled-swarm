import ast
import os
import signal
import sys
import threading
from enum import Enum
from functools import partial
from subprocess import PIPE, run
from threading import Thread
from typing import Dict, List, Optional, Self, Tuple, Type


class Struct:
    """Emulate the stdclass of PHP."""

    def __init__(self: Self, **entries: Dict[str, any]) -> Self:
        """_summary_

        Args:
            self (Self): Create all the data members based
                         on the keyword arguments.
            entries (Dict[str, any]): key/value sequence for the variables
                                      to create as data-member of this object.

        Returns:
            Self: Struct instance.
        """
        self.__dict__.update(entries)


def threaded(func: callable) -> Thread:
    """Decorator that multithreading the target function
       with the given parameters.

    Args:
        func (callable): execute in a separate thread.

    Returns:
        Thread: created for the function.
    """

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args)
        thread.start()
        return thread

    return wrapper


class EnumList(Enum):
    """Add to Enum a method to get the list of all the values."""

    @classmethod
    def list(cls: Type[Self]) -> List[any]:
        """All values of this enum as list.

        Args:
            cls (Type[Self]): class type.

        Returns:
            List[any]: all the values.
        """
        return list(map(lambda c: c.value, cls))


def execute(cmd: str, logger: any, min_lines_warning: int,
            error_if: List[str] = [], test: bool = False) -> Tuple[int, list]:
    """Execute a program and write with the logger the result.

    Args:
        cmd (str): command to execute.
        logger (any): write the output.
        min_lines_warning (int): minimum number of lines to log as
                                 warning (if equal to -1 warning disabled).
        error_if (List[str]): log error if present one of these texts
                              in the command output.
        test (bool): if True only print to log the command without execution.

    Returns:
        Tuple[int, list]: code and output lines of the command
    """
    if not test:
        _result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        _res_stdout = list(filter(None, _result.stdout.split("\n")))
        _res_stderr = list(filter(None, _result.stderr.split("\n")))
        if _result.returncode != 0:
            _callback = logger.error
        elif min_lines_warning > -1 and len(_res_stdout) >= min_lines_warning:
            _callback = logger.warning
        elif min_lines_warning == -1:
            _callback = logger.info
        else:
            _callback = logger.success
        for r in _res_stdout + _res_stderr:
            for _e in error_if:
                if _e in r:
                    _callback = logger.error
                    break
        for r in _res_stdout + _res_stderr:
            _callback(r)
        return _result.returncode, _res_stdout
    else:
        logger.info(f"Execution of cmd: {cmd}")
        return 0, ""


def keyboard_interrupt(callback: callable, return_code: Optional[int] = 0, waiting: bool = True) -> None:
    """Manage the interruption of a script execution
       with the keyboard press event.

    Args:
        callback (callable): executed after the interruption
        return_code (Optional[int], optional): if not None exit
                                               the program with this code
        waiting (bool, optional): wait the keyword interruption.
                                  Defaults to True.
    """

    def _handler(signal, frame):
        print("\r", end="")  # To present "^C" in the stdout.
        callback()
        if return_code is not None:
            sys.exit(return_code)

    signal.signal(signal.SIGINT, _handler)
    if waiting:
        _forever = threading.Event()
        _forever.wait()


def get_classes(file_path: str, with_module_name: bool = False) -> List[str]:
    """Get all the python classes found in a file.

    Args:
        file_path (str): path of the file to get the python classes.
        with_module_name (bool, optional): add the module name as prefix to the
                                           found classes. Defaults to False.

    Raises:
        SyntaxError: if the file if not valid.

    Returns:
        List[str]: of classes found in the file.
    """
    if file_path.endswith(".py"):
        with open(file_path, "r") as _src:
            _parse = ast.parse(_src.read())
            if with_module_name:
                module_name, _ = os.path.splitext(os.path.basename(file_path))
                _with_module_name = f"{module_name}."
            else:
                _with_module_name = ""
            return [
                f"{_with_module_name}{node.name}"
                for node in ast.walk(_parse)
                if isinstance(node, ast.ClassDef)
            ]
    else:
        raise SyntaxError(f"{file_path} not valid")


def get_class_methods(file_path: str, with_class_name: bool = False) -> List[str]:
    """Get all the python class methods found in a file.

    Args:
        file_path (str): path of the file to get the python class methods.
        with_class_name (bool, optional): add the class name as prefix to the
                                        found class methods. Defaults to False.

    Raises:
        SyntaxError: if the file if not valid.

    Returns:
        List[str]: of class methods found in the file.
    """
    if file_path.endswith(".py"):
        with open(file_path, "r") as _src:
            _parse = ast.parse(_src.read())
            out = []
            for node in ast.walk(_parse):
                if isinstance(node, ast.ClassDef):
                    _with_class_name = f"{node.name}." if with_class_name else ""
                    out += [f"{_with_class_name}{inner_node.name}"
                            for inner_node in ast.walk(node)
                            if isinstance(inner_node, ast.FunctionDef)]
            return out
    else:
        raise SyntaxError(f"{file_path} not valid")


def nothing():
    """Do nothing."""
    pass


def exit_handler(logger: any, additional_callback: callable = nothing) -> callable:
    """Exit handler.

    Args:
        logger (any): logger instance.
        additional_callback (callable, optional): . Defaults to nothing.

    Returns:
        callable: the function to execute based on the handler.
    """

    def _exit():
        """Internal function used as return for the handler."""
        logger.warning("Terminating...")
        additional_callback()

    return _exit


def handler(func: callable) -> Thread:
    """Decorator that wrap a function.

    Args:
        func (callable): wrapped.

    Returns:
        the called function reference.
    """

    def _handler(*args: List[any], **kwargs: Dict[str, any]) -> any:
        """Execute the function.

        Args:
            args (List[any]): function arguments.
            kwargs (Dict[str, any]): function keyword arguments.

        Returns:
            any: depending on the wrapped function return.
        """
        return partial(func, *args, **kwargs)

    return _handler


handler_type = partial


def strip(data: str, sep: str = "\n") -> List[str]:
    """Strip the string in list based on the
       separator and remote the empty ones.

    Args:
        data (str): string to strip.
        sep (str, optional): separator. Defaults to "\n".

    Returns:
        List[str]: list of string divided by separator.
    """
    return list(filter(None, data.strip().split(sep)))


def ds(*params: List[any]) -> callable:
    """TODO: _summary_

    Returns:
        callable: _description_
    """
    def decorator(obj):
        obj.__doc__ = obj.__doc__.format(*params)
        return obj

    return decorator


clize_ds_vt = """
    :param verbose: to log the variables.
    :param test: to apply the script without permanent results.
    :param plain: to log in a plain mode or with detailed info.
"""
