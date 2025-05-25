import numpy as np

qname_list = [
    "google.it",
    "nyc.com",
    "nba.com",
    "gazzetta.it",
    "bbc.co.uk",
    "example.com",
    "fake.it",
    "test.com",
]


class __base:
    count = [-1]
    show = True
    duration_seconds = 30 * 60
    ip_source = ["172.22.1.1/16"]
    ip_dest = ["172.22.1.1"]
    interval = [1.0 / 20]


class dns(__base):
    kind = "dns"
    qname = qname_list


class ntp(__base):
    kind = "ntp"
    payload_size = 4


class rtmp(__base):
    kind = "rtmp"


class http(__base):
    kind = "http"
    url_path = "index.html"


class https(__base):
    kind = "https"
    url_path = "page.html"


class __demo(__base):
    kind = "general"
    transport = "tcp"
    interval = [1.0 / 200]


class demo(__demo):
    port_dest = [80, 1935, 1936, 2395, 443]
    payload_size_range = [500, 1200]


class demo_2(__demo):
    ip_source = ["10.1.2/8"]
    port_dest = [80, 1935, 1936, 2395, 443, 53]
    payload_size_range = [400, 1000]


class demo_3(demo_2):
    ip_source = ["12.3.2/16"]
    payload_size_range = [200, 1200]


class __demo_deme_dns(dns):
    show = False
    ip_dest = ["172.22.3.3"]
    ip_source = [f"172.22.{x}.{x}" for x in [4, 5, 6, 7, 8, 9, 10]]


class __demo_deme_ntp(ntp, __demo_deme_dns):
    show = False
    ip_dest = ["172.22.1.1"]
    ip_source = [f"172.22.{x}.{x}" for x in [4, 5, 6, 7, 8, 9, 10]]


class demo_deme_dns_normal(__demo_deme_dns):
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


class demo_deme_ntp_normal(__demo_deme_ntp, demo_deme_dns_normal):
    payload_size = [4] * len(demo_deme_dns_normal.ref)


class demo_deme_dns_attack(__demo_deme_dns):
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


class demo_deme_ntp_attack(__demo_deme_ntp, demo_deme_dns_attack):
    payload_size = [4] * len(demo_deme_dns_attack.ref)


class demo_deme_dns_background(demo):
    show = False
    ip_source = [f"172.22.{x}.{x}" for x in [4, 5, 6, 7, 8, 9, 10]]
    ip_dest = ["172.22.3.3"]


class demo_deme_ntp_background(demo_deme_dns_background):
    ip_dest = ["172.22.1.1"]


pkt_rate_normal = 1000


class demo_dns_normal(dns):
    duration_seconds = 240
    ip_source = ["192.168.130.1", "192.168.130.2", "192.168.130.3", "192.168.130.4",
                 "192.168.130.5", "192.168.130.6", "192.168.130.7", "192.168.130.8",
                 "192.168.130.9", "192.168.130.10"]
    ip_dest = ["192.168.130.17"]
    transport = "udp"
    interval = [1.0 / pkt_rate_normal]


class demo_streaming_normal(__base):
    duration_seconds = 240
    port_dest = [80, 443]
    ip_source = ["192.168.130.1", "192.168.130.2", "192.168.130.3", "192.168.130.4",
                 "192.168.130.5", "192.168.130.6", "192.168.130.7", "192.168.130.8",
                 "192.168.130.9", "192.168.130.10"]
    ip_dest = ["192.168.130.45", "192.168.130.19"]
    transport = "tcp"
    kind = "general"
    interval = [1.0 / pkt_rate_normal]


pkt_rate_attack = 1000 * 100


class demo_dns_attack(demo_dns_normal):
    interval = [1.0 / pkt_rate_attack]


class demo_streaming_attack(demo_streaming_normal):
    interval = [1.0 / pkt_rate_attack]
