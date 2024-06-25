import lib
from log import logger
from packets import Profile
from scapy.all import send


def generator(*, profile_class_path: "p" = "profile"):  # noqa: F821
    """
    HORSE Traffic Generator

    Generate  packets
    """
    profile = lib.load_class(profile_class_path)
    Profile.validate(profile)
    kind = lib.load_class(f"packets.{profile.kind}")
    for interval, count in zip(profile.interval, profile.count):
        logger.info(f"interval: {interval} - count: {count}")
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
