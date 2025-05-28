import random
import re

from config import get_settings
from log import logger
from scapy.all import IP, TCP, UDP, rdpcap, wrpcap

pkt_dirs = ["src", "dst"]
l4_protos = [TCP, UDP]


def inverse_pkt_dir(pkt_dir: str) -> str:
    return pkt_dirs[0] if pkt_dir == pkt_dirs[1] else pkt_dirs[1]


def get_last_reply_ip(buffer_ips: list, random_values: list) -> str:
    if len(buffer_ips) > 0:
        return buffer_ips.pop()
    else:
        return random.choices(random_values)[0]


def manager(*, config: "c" = "manager.toml"):  # noqa: F821
    """PCAP file Managers

    :param config: Path of the configuration file.
    """
    logger.info(f"Config: {config}")
    settings = get_settings(config)

    for input_file, output_file in settings.pcap.files.items():
        logger.info(f"Input file: {input_file}")

        packets = rdpcap(input_file)
        modified_packets = []

        buffer_ips = {pkt_dirs[0]: [], pkt_dirs[1]: []}

        pkt_idx = 0
        for packet in packets:
            pkt_idx += 1
            if packet.haslayer(IP):
                logger.info(f"{pkt_idx} IP src {packet[IP].src} dst {packet[IP].dst}")
                for pkt_dir in pkt_dirs:
                    for _, ip_pattern in settings.ip.replace[pkt_dir].target.items():
                        if re.search(ip_pattern, getattr(packet[IP], pkt_dir)):
                            ip_new = random.choices(settings.ip.replace[pkt_dir].random.values())[0]
                            buffer_ips[pkt_dir].insert(0, ip_new)
                            setattr(packet[IP], pkt_dir, ip_new)
                            del packet[IP].chksum  # Remove the checksum so Scapy recalculates it
                            logger.success(f"{pkt_idx} IP {pkt_dir} {ip_pattern} => {ip_new}")
                    for _, ip_pattern in settings.ip.reply_last[pkt_dir].items():
                        if re.search(ip_pattern, getattr(packet[IP], pkt_dir)):
                            inv_pkt_dir = inverse_pkt_dir(pkt_dir)
                            inv_ip_new = get_last_reply_ip(buffer_ips[inv_pkt_dir],
                                                           settings.ip.replace[pkt_dir].random.values())
                            ip_new = get_last_reply_ip(buffer_ips[pkt_dir],
                                                       settings.ip.replace[inv_pkt_dir].random.values())

                            setattr(packet[IP], inv_pkt_dir, inv_ip_new)
                            setattr(packet[IP], pkt_dir, ip_new)
                            del packet[IP].chksum  # Remove the checksum so Scapy recalculates it
                            logger.success(f"{pkt_idx} IP {pkt_dir} {ip_pattern} => {ip_new}")
            for l4_proto in l4_protos:
                if packet.haslayer(l4_proto):
                    del packet[l4_proto].chksum  # For L4 Proto packets, remove the checksum for recalculation
            remove_packet = False
            for pkt_dir in pkt_dirs:
                for _, ip_pattern in settings.ip.delete[pkt_dir].items():
                    if re.search(ip_pattern, getattr(packet[IP], pkt_dir)):
                        remove_packet = True
                        logger.success(f"{pkt_idx} with ip {pkt_dir} = {ip_pattern} removed")
                        break
            if not remove_packet:
                modified_packets.append(packet)

        wrpcap(output_file, modified_packets)
        logger.success(f"Output file: {output_file}")
