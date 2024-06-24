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
