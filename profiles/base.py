from scapy.all import IP, UDP, TCP, Packet, Raw, Ether
from typing import List, Self


class base_profile:
    # Default: False, to show detailed information of profile during execution.
    verbose: bool

    # Default: False, don't send packets, only show what would be sent.
    test: bool

    # Default: False, show scapy output during execution.
    show: bool

    # Network interface to use for sending packets.
    interface: str

    # List of packet counts to send at each interval.
    count: List[int]

    # List of intervals in seconds between sending packets.
    interval_seconds: List[float]

    # Total duration in seconds for profile execution.
    duration_seconds: int

    # Destination IP addresses for packets (usually are victims of attacks or
    # they can be senders of real attacks when we impersonate victims).
    dst_ip: str | List[str]

    # Source IP addresses for packets (used when we want to impersonate victims of attacks).
    src_ip: str | List[str]

    # Source ports for packets (TCP or UDP - used when we want to impersonate victim of attacks).
    src_port: int | List[int]

    # Destination ports for packets (TPC or UDP - usually are victims of attacks or
    # they can be senders of real attacks when we impersonate victims
    dst_port: int | List[int]

    # It is necessary to implement the create method to generate the packets following the Scapy format.
    # See https://scapy.readthedocs.io/en/latest/ for more details on creating packets with Scapy.

    def create(self: Self) -> Packet:
        """
        Example of TCP packets
        """
        layer_2 = Ether()
        layer_3 = IP(src=self.src_ip, dst=self.dst_ip)
        layer_4 = TCP(sport=self.src_port, dport=self.dst_ports)
        data: str  # Some data for the payload
        return layer_2 / layer_3 / layer_4 / Raw(load=data)

    def create(self: Self) -> Packet:
        """
        Example of UDP packets
        """
        layer_2 = Ether()
        layer_3 = IP(src=self.src_ip, dst=self.dst_ip)
        layer_4 = UDP(sport=self.src_port, dport=self.dst_ports)
        data: str  # Some data for the payload
        return layer_2 / layer_3 / layer_4 / Raw(load=data)
