import numpy as np


class __demo:
    show = False
    kind = "general"
    transport = "tcp"
    interval = [1.0 / 200]
    payload_size_range = [500, 1200]
    port_dest = [80, 1935, 1936, 2395, 443, 53]
    ip_dest = ["10.8.0.100"]  # HOLO Alex OVPN Profile
    # ip_dest = ["10.8.0.102"]  # HOLO Laptop OVPN Profile


class demo_ntp_normal(__demo):
    show = False
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
    interval = list(120 / ref)


class demo_ntp_attack_ps500_1200(__demo):
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
    interval = list(120 / ref)


class demo_ntp_attack_ps2k_3k(demo_ntp_attack_ps500_1200):
    payload_size_range = [2000, 3000]


class demo_ntp_attack_ps3k_4k(demo_ntp_attack_ps2k_3k):
    payload_size_range = [3000, 4000]
