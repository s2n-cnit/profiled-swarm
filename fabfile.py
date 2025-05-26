from fabric.api import cd, env, run

code_dir = "$HOME/profiled-swarm"


def requirements():
    if run("command -v python3.12").failed:
        run("curl -s https://raw.githubusercontent.com/markelog/ec-install/master/scripts/install.sh | sh")
        run("ec python@3.12")
        run("pip install poetry")


def deploy():
    if run("command -v git").failed:
        run("sudo apt install -y git")
    if run(f"test -d {code_dir}").failed:
        run(f"git clone https://github.com/s2n-cnit/profiled-swarm.git {code_dir}")
    with cd(code_dir):
        run("poetry install")


def generate(profile: str):
    with cd(code_dir):
        run("sudo su")
        run(f"poetry run python profiled-swarm.py -p profile.{profile}")


# HPING3 alternative solution

set_ue_a = [x + ".ueransim.5g.horse.s2n-cnit" for x in range(1, 6)]
set_ue_b = [x + ".ueransim.5g.horse.s2n-cnit" for x in range(6, 11)]

env.roledefs = {
    'streaming_a': set_ue_a,
    'streaming_b': set_ue_b,
    'streaming_c': set_ue_a,
    'streaming_d': set_ue_b,
    'dns': set_ue_a + set_ue_b
}


def hping3_gen(dst_ip: str, dst_port: int, packet_size: int, packet_count: int, speed: str, protocol: str):
    run(f"hping3 -c {packet_count} {speed} {protocol} -p {dst_port} {dst_ip} -d {packet_size}")


def hping3_gen_streaming_a_normal():
    hping3_gen(dst_ip="192.168.130.45", dst_port=80, packet_size=200,
               packet_count=20000, speed="-i u100", protocol="-2")


def hping3_gen_streaming_b_normal():
    hping3_gen(dst_ip="192.168.130.45", dst_port=443, packet_size=200,
               packet_count=20000, speed="-i u100", protocol="-2")


def hping3_gen_streaming_c_normal():
    hping3_gen(dst_ip="192.168.130.19", dst_port=80, packet_size=200,
               packet_count=20000, speed="-i u100", protocol="-2")


def hping3_gen_streaming_d_normal():
    hping3_gen(dst_ip="192.168.130.19", dst_port=443, packet_size=200,
               packet_count=20000, speed="-i u100", protocol="-2")


def hping3_gen_streaming_a_attack():
    hping3_gen(dst_ip="192.168.130.45", dst_port=80, packet_size=200,
               packet_count=200000, speed="--faster", protocol="-2")


def hping3_gen_streaming_b_attack():
    hping3_gen(dst_ip="192.168.130.45", dst_port=443, packet_size=200,
               packet_count=200000, speed="--faster", protocol="-2")


def hping3_gen_streaming_c_attack():
    hping3_gen(dst_ip="192.168.130.19", dst_port=80, packet_size=200,
               packet_count=200000, speed="--faster", protocol="-2")


def hping3_gen_streaming_d_attack():
    hping3_gen(dst_ip="192.168.130.19", dst_port=443, packet_size=200,
               packet_count=200000, speed="-faster", protocol="-2")


def hping3_gen_dns_normal():
    hping3_gen(dst_ip="192.168.130.17", dst_port=53, packet_size=200,
               packet_count=20000, speed="-i u100", protocol="-2")


def hping3_gen_dns_attack():
    hping3_gen(dst_ip="192.168.130.19", dst_port=53, packet_size=200,
               packet_count=200000, speed="-faster", protocol="-2")
