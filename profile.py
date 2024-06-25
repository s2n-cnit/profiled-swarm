import numpy as np


class __base:
    count = -1
    show = True
    duration_seconds = 30 * 60
    ip_source = "172.22.1.1/16"
    ip_dest = "172.22.1.1"
    interval = 1.0 / 20


class dns(__base):
    kind = "dns"
    qname = "google.it"


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
    interval = 1.0 / 200


class demo(__demo):
    port_dest = [80, 1935, 1936, 2395, 443]
    payload_size_range = [500, 1200]


class demo_2(__demo):
    ip_source = "10.1.2/8"
    port_dest = [80, 1935, 1936, 2395, 443, 53]
    payload_size_range = [400, 1000]


class demo_3(demo_2):
    ip_source = "12.3.2/16"
    payload_size_range = [200, 1200]


class __demo_deme_dns(dns):
    ip_dest = "172.22.3.3"


class demo_deme_dns_normal(__demo_deme_dns):
    interval = 1.0 / 10


class demo_deme_dns_attack(__demo_deme_dns):
    interval = (
        1.0
        / 120
        * np.array(
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
    )
