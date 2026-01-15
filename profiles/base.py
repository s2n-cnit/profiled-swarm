from scapy.all import Packet
from typing import List


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

    def create(self) -> Packet:
        """
        Create and return a scapy Packet object to be sent.
        See https://scapy.readthedocs.io/en/latest/ for more details on creating packets with Scapy.
        """
        pass
