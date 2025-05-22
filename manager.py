import re

from config import get_settings
from scapy.all import IP, TCP, UDP, rdpcap, wrpcap

pkt_dirs = ["src", "dst"]
l4_protos = [TCP, UDP]


def manager(*, config: "c" = "manager.toml"):  # noqa: F821
    """PCAP file Manager

    :param config: Path of the configuration file.
    """
    settings = get_settings(config)

    for input_file, output_file in settings.pcap.files.items():
        packets = rdpcap(input_file)
        modified_packets = []

        for packet in packets:
            if packet.haslayer(IP):
                for pkt_dir in pkt_dirs:
                    for ip_pattern, ip_new in settings.ip.replace[pkt_dir].items():
                        if re.search(ip_pattern, packet[IP][pkt_dir]):
                            packet[IP][pkt_dir] = ip_new
                            del packet[IP].chksum  # Remove the checksum so Scapy recalculates it
            for l4_proto in l4_protos:
                if packet.haslayer(l4_protos):
                    del packet[l4_protos].chksum  # For L4 Proto packets, remove the checksum for recalculation
            remove_packet = False
            for pkt_dir in pkt_dirs:
                for ip_pattern in settings.ip.delete[pkt_dir]:
                    if re.search(ip_pattern, packet[IP][pkt_dir]):
                        remove_packet = True
                        break
            if not remove_packet:
                modified_packets.append(packet)

        wrpcap(output_file, modified_packets)
