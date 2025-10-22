import lib
from log import logger
from packets import Profile
from scapy.all import send
from utils import keyboard_interrupt
import random


def _exit():
    logger.warning("Terminating...")


def generator(*, profile_class_path: "p" = "profile",  # noqa: F821
              **kwargs: ...):  # noqa: F821
    """
    HORSE Traffic Generator

    Generate packets

    :param profile_class_path: path of the profile class to use
    :param dest: destination IP addresses
    """
    profile = lib.load_class(profile_class_path)
    Profile.validate(profile, kwargs)
    kind = lib.load_class(f"packets.{profile.kind}")
    keyboard_interrupt(_exit, return_code=1, waiting=False)
    if hasattr(profile, "payload_size"):
        payload_size_list = lib.make_iter(profile.payload_size)
    else:
        payload_size_list = [1] * len(profile.interval)
    if hasattr(profile, "payload_size_range"):
        ps_min, ps_max = profile.payload_size_range
        payload_size_list = [
            random.randint(ps_min, ps_max + 1) for _ in range(len(profile.interval))
        ]
    for interval, count, payload_size in zip(profile.interval, profile.count,
                                             payload_size_list):
        logger.info(f"kind: {profile.kind} - "
                    f"interval: {interval} - count: {count} - "
                    f"payload size: {payload_size}")
        profile.payload_size = payload_size
        pkts = kind(profile)
        if profile.show:
            pkts.show()
        if not profile.test:
            send(
                pkts,
                count=count,
                loop=count == -1,
                inter=interval,
            )
