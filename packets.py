import signal
import sys
from enum import Enum
from random import choice, randint, seed
from typing import Any, Self, Type

from lib import duration_end, make_iter
from log import Error, logger
from scapy.all import DNS, DNSQR, ICMP, IP, TCP, UDP, RandString, Raw

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
        "ip_source",
        "ip_dest",
        "count",
        "interval",
        "kind",
        "duration_seconds",
    ]

    __optional_fields = {"test": False, "show": False}

    @staticmethod
    def validate(cls: Type[Self]):
        for f in Profile.__required_fields:
            if not hasattr(cls, f):
                logger.error(f"Profile {cls.__name__} not define field {f}")
                sys.exit(Error.NOT_FIELD_PROFILE)
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


def __check_field(
    profile: object, field: str, transform: callable = lambda x: x
) -> None:
    if not hasattr(profile, field):
        logger.error(f"Field {field} not found in profile {profile.kind}")
        sys.exit(Error.NOT_FIELD_PROFILE)
    setattr(profile, field, transform(getattr(profile, field)))


def __ip(profile: object) -> IP:
    return IP(src=choice(profile.ip_source), dst=choice(profile.ip_dest))


def dns(profile: object) -> Any:
    __check_field(profile, field="qname", transform=make_iter)
    return (
        __ip(profile)
        / UDP(dport=53)
        / DNS(rd=1, qd=DNSQR(qname=choice(profile.qname)))
    )


def icmp(profile: object) -> Any:
    return __ip(profile) / ICMP()


def __http(profile: object, name: str, dport: int):
    __check_field(profile, field="url_path")
    return (
        __ip(profile)
        / TCP(dport=dport)
        / f"GET /{profile.url_path} HTTP/1.0 \n\n"
    )


def http(profile: object) -> Any:
    return __http(profile, "http", dport=80)


def https(profile: object) -> Any:
    return __http(profile, "http", dport=443)


def rtsp(profile: object) -> Any:
    return __ip(profile) / TCP(dport=554)


def rtmp(profile: object) -> Any:
    return __ip(profile) / TCP(dport=[80, 1935, 1936])


def rtmps(profile: object) -> Any:
    return __ip(profile) / TCP(dport=[2395, 443])


def apple_bonjour(profile: object) -> Any:
    return __ip(profile) / TCP(dport=5353)


def ntp(profile: object) -> Any:
    __check_field(profile, field="payload_size")
    payload = "\x1b\x00\x00\x00" + "\x00" * max(11 * 4, profile.payload_size)
    return __ip(profile) / UDP(sport=80, dport=123) / Raw(load=payload)


def general(profile: object) -> Any:
    __check_field(profile, field="port_dest")
    __check_field(profile, field="transport")
    __check_field(profile, field="payload_size_range")
    seed()
    match profile.transport:
        case "tcp":
            layer4 = TCP
        case "udp":
            layer4 = UDP
    return (
        __ip(profile)
        / layer4(dport=profile.port_dest)
        / Raw(RandString(size=randint(*profile.payload_size_range)))
    )


class Kind(str, Enum):
    DNS = "dns"
    ICMP = "icmp"
    HTTP = "http"
    HTTPS = "https"
    RTSP = "rtsp"
    RTMP = "rtmp"
    RTMPS = "rtmps"
    APPLE_BONJOUR = "apple_bonjour"
    GENERAL = "general"
    NTP = "ntp"
