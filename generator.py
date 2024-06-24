import lib
from scapy.all import send


def generator(*, profile_class_path: "p" = "profile"):  # noqa: F821
    """
    HORSE Traffic Generator

    Generate  packets
    """
    profile = lib.load_class(profile_class_path)
    lib.Profile.validate(profile)
    kind = lib.load_class(f"packets.{profile.kind}")
    pkts = kind(profile)
    if profile.show:
        pkts.show()
    if not profile.test:
        send(
            pkts,
            count=profile.count,
            loop=profile.count == -1,
            inter=profile.interval,
        )
