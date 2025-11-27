import lib
from log import logger
from profile import Profile
from scapy.all import send
from utils import keyboard_interrupt


def _exit():
    logger.warning("Terminating...")


def generator(*, profile_class_path: "p" = "profile"):  # noqa: F821
    """
    HORSE Traffic Generator

    Generate packets

    :param profile_class_path: path of the profile class to use
    """
    profile = lib.load_class(profile_class_path)
    Profile.validate(profile)
    _p = profile()
    keyboard_interrupt(_exit, return_code=1, waiting=False)
    for interval_seconds, count in zip(_p.interval_seconds, _p.count):
        logger.info(f"interval: {interval_seconds} - count: {count}")
        pkts = _p.create()
        if _p.show:
            pkts.show()
        if not _p.test:
            send(
                pkts,
                count=count,
                loop=count == -1,
                inter=interval_seconds,
                verbose=_p.verbose
            )
