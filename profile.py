import numpy as np


class __demo:
    show = False
    kind = "general"
    transport = "tcp"
    interval = [1.0 / 200]
    payload_size_range = [500, 1200]
    port_dest = [80, 1935, 1936, 2395, 443, 53]
    ip_dest = ["192.168.130.45"]


class demo_ntp_normal(__demo):
    show = False
    ref = np.array(
        [
            33.82097685,
            32.5762677,
            33.68583422,
            33.02180128,
            34.31683965,
            33.01941864,
            33.3951162,
            34.8044961,
            34.82896227,
            32.76013208,
            34.66339299,
            34.05555319,
            33.568511,
            34.19197836,
            33.69126809,
            34.52364965,
        ]
    )
    count = list(map(round, ref))
    interval = list(120 / ref)


class demo_ntp_attack(__demo):
    ref = np.array(
        [
            33.95149936,
            33.79847654,
            33.23726486,
            34.92724149,
            38.06783745,
            46.35609054,
            61.69733684,
            75.76723206,
            80.19098465,
            76.72654594,
            61.35187954,
            49.45015471,
            38.59728894,
            35.93740773,
            34.7416466,
            34.83174674,
        ]
    )
    count = list(map(round, ref))
    interval = list(120 / ref)
