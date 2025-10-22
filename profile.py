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
    duration_seconds = 2 * 60 * len(ref)


class demo_ntp_attack_ps500_1200_pm3k(__demo):
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
    duration_seconds = 2 * 60 * len(ref)


class demo_ntp_attack_ps2k_3k_pm3k(demo_ntp_attack_ps500_1200_pm3k):
    payload_size_range = [2000, 3000]


class demo_ntp_attack_ps3k_4k_pm3k(demo_ntp_attack_ps500_1200_pm3k):
    payload_size_range = [3000, 4000]


class demo_ntp_attack_ps500_1200_pm5k(demo_ntp_attack_ps500_1200_pm3k):
    ref = np.array(
        [
            26,
            1000,
            5000,
            5000,
            5000
        ]
    )
    interval = list(120 / ref)


class demo_ntp_attack_ps2k_3k_pm5k(demo_ntp_attack_ps500_1200_pm5k):
    payload_size_range = [2000, 3000]


class demo_ntp_attack_ps3k_4k_pm5k(demo_ntp_attack_ps500_1200_pm5k):
    payload_size_range = [3000, 4000]


class demo_ntp_attack_ps500_1200_pm7k(demo_ntp_attack_ps500_1200_pm5k):
    ref = np.array(
        [
            26,
            1000,
            7000,
            7000,
            7000
        ]
    )
    interval = list(120 / ref)


class demo_ntp_attack_ps2k_3k_pm7k(demo_ntp_attack_ps500_1200_pm5k):
    payload_size_range = [2000, 3000]


class demo_ntp_attack_ps3k_4k_pm7k(demo_ntp_attack_ps500_1200_pm5k):
    payload_size_range = [3000, 4000]


class demo_ntp_attack_ps500_1200_pm10k(demo_ntp_attack_ps500_1200_pm7k):
    ref = np.array(
        [
            26,
            1000,
            7000,
            7000,
            7000
        ]
    )
    interval = list(120 / ref)


class demo_ntp_attack_ps2k_3k_pm10k(demo_ntp_attack_ps500_1200_pm7k):
    payload_size_range = [2000, 3000]


class demo_ntp_attack_ps3k_4k_pm10k(demo_ntp_attack_ps500_1200_pm7k):
    payload_size_range = [3000, 4000]
