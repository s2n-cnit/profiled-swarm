import sys
from enum import Enum
from random import randint, seed
from typing import Any

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


def __check_field(profile: object, field: str) -> None:
    if not hasattr(profile, field):
        logger.error(f"Field {field} not found in profile {profile.kind}")
        sys.exit(Error.NOT_FIELD_PROFILE)


def __ip(profile: object) -> IP:
    return IP(src=profile.ip_source, dst=profile.ip_dest)


def dns(profile: object) -> Any:
    __check_field(profile, field="qname")
    return (
        __ip(profile)
        / UDP(dport=53)
        / DNS(rd=1, qd=DNSQR(qname=profile.qname))
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
