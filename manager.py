import re

from config import get_settings
from log import logger
from scapy.all import IP, TCP, UDP, rdpcap, wrpcap

pkt_dirs = ["src", "dst"]
l4_protos = [TCP, UDP]


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

        pkt_idx = 0
        for packet in packets:
            pkt_idx += 1
            if packet.haslayer(IP):
                logger.info(f"{pkt_idx} IP src {packet[IP].src} dst {packet[IP].dst}")
                for pkt_dir in pkt_dirs:
                    for ip_pattern, ip_new in settings.ip.replace[pkt_dir].items():
                        if re.search(ip_pattern, getattr(packet[IP], pkt_dir)):
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
        logger.success(f"Output file: {input_file}")
