from fabric import Connection, ThreadingGroup, task

set_ue_a = [str(x) + ".ueransim.5g.horse.s2n-cnit" for x in range(1, 6)]
set_ue_b = [str(x) + ".ueransim.5g.horse.s2n-cnit" for x in range(6, 11)]


kwargs = {
    "password": 'ubuntu',
}

groups = dict(normal=ThreadingGroup(*set_ue_a, user="ubuntu", connect_kwargs=kwargs),
              attack=ThreadingGroup(*set_ue_b, user="ubuntu", connect_kwargs=kwargs))


def set_groups(group_key: str | list):
    if isinstance(group_key, str):
        return [group_key]
    return group_key


def hping3_gen(dst_ip: str, dst_port: int, packet_size: int, packet_count: int, speed: str, protocol: str) -> str:
    return f"hping3 -c {packet_count} {speed} {protocol} -p {dst_port} {dst_ip} -d {packet_size}"


core_upf_ip = "192.168.130.45"
edge_upf_ip = "192.168.130.19"
dns_ip = "192.168.130.17"
packet_size = 200

streaming_port_a = 80
streaming_port_b = 443
dns_port = 53

packet_size = 200
packet_count = 10 * 1000 * 1000

speed_normal = "-i u1000"
speed_attack = "-i u100"

proto_tcp = "-2"


@task
def requirements(c: Connection) -> None:
    for g in set_groups(['normal', 'attack']):
        groups[g].sudo("apt install hping3")


@task
def hping3_gen_streaming_a_normal_core(c: Connection, dst_ip: str = core_upf_ip, dst_port: int = streaming_port_a,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_normal,
                                       ue_group: str | list = "normal"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_streaming_b_normal_core(c: Connection, dst_ip: str = core_upf_ip, dst_port: int = streaming_port_b,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_normal,
                                       ue_group: str | list = "normal"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_streaming_a_normal_edge(c: Connection, dst_ip: str = edge_upf_ip, dst_port: int = streaming_port_a,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_normal,
                                       ue_group: str | list = "normal"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_streaming_b_normal_edge(c: Connection, dst_ip: str = edge_upf_ip, dst_port: int = streaming_port_b,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_normal,
                                       ue_group: str | list = "normal"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_streaming_a_attack_core(c: Connection, dst_ip: str = core_upf_ip, dst_port: int = streaming_port_a,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_attack,
                                       ue_group: str | list = "attack"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_streaming_b_attack_core(c: Connection, dst_ip: str = core_upf_ip, dst_port: int = streaming_port_b,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_attack,
                                       ue_group: str | list = "attack"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_streaming_a_attack_edge(c: Connection, dst_ip: str = edge_upf_ip, dst_port: int = streaming_port_a,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_attack,
                                       ue_group: str | list = "attack"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_streaming_b_attack_edge(c: Connection, dst_ip: str = edge_upf_ip, dst_port: int = streaming_port_b,
                                       packet_size: int = packet_size, packet_count: int = packet_count,
                                       speed: str = speed_attack,
                                       ue_group: str | list = "attack"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_dns_normal(c: Connection, dst_ip: str = dns_ip, dst_port: int = dns_port,
                          packet_size: int = packet_size, packet_count: int = packet_count,
                          speed: str = speed_normal,
                          ue_group: str | list = "normal"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))


@task
def hping3_gen_dns_attack(c: Connection, dst_ip: str = dns_ip, dst_port: int = dns_port,
                          packet_size: int = packet_size, packet_count: int = packet_count,
                          speed: str = speed_attack,
                          ue_group: str | list = "attack"):
    for g in set_groups(ue_group):
        groups[g].sudo(hping3_gen(dst_ip=dst_ip, dst_port=dst_port, packet_size=packet_size,
                                  packet_count=packet_count, speed=speed, protocol=proto_tcp))
