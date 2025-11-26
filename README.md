# Profiled Swarm

> Generator of Targeted Traffic with Profiles

Profiled Swarm is a robust Python framework designed to generate highly realistic, targeted network traffic based on configurable behavioral profiles. The core purpose of this tool is to simulate complex, real-world network environments, such as a "swarm" of users, devices, or bots, interacting with specific services.

This capability is essential for researchers and engineers performing network security experiments, performance testing, and validating IDS[^1] against high-fidelity, stateful traffic scenarios.

# Key Features

1. **Profile-Driven Generation**: the system uses configuration files to define complex stateful behaviors, including inter-packet timing distributions (known as think time), precise protocol sequences (like a TCP[^2] handshake followed by an HTTP[^3] request), and dynamically varying payload sizes. This ensures the generated traffic accurately mimics real user behavior.
2. **Swarm Management**: you can coordinate multiple, simultaneous traffic generators from a centralized manager. This allows a single control point to launch a heterogeneous mix of traffic streams, simulating an entire segment of a corporate or residential network, rather than just one machine.
3. **Targeted Traffic**: the tool supports easy specification of target IP addresses, ports, and protocols for focused experimentation. You can control interactions across the network stack, from Layer 3 (IP) up to application-layer protocols.
4. **Modular and Extensible**: the framework is built on clear Python components, making it simple to extend or integrate new protocols and behavioral models.

# Quick Start: Installation

Profiled Swarm uses a two-part approach for dependency management and execution: _poetry_ defines the project structure and dependencies, while _uv_ handles installation and running.

> [!TIP]
> We strongly recommend this combination because _uv_ is a modern, high-performance tool that resolves package conflicts and installs environments significantly faster and with fewer common system-level problems than traditional Python package managers.

## Prerequisites

1. You must have _Python 3.8+ installed.
2. You need uv (for reliable installation and execution). Install it globally:

```shell
pip install uv
```

## Setup Steps

1. **Clone the Repository**: begin by cloning the project files to your local machine:

```shell
git clone [https://github.com/s2n-cnit/profiled-swarm.git](https://github.com/s2n-cnit/profiled-swarm.git)
cd profiled-swarm
```

2. **Setup the virtual environment**:

```shell
uv venv
```

## Basic Usage

1. Pass the profile class path using the options <kbd>-p</kdb>.

```shell
uv run profiled-swarm.py -p profiles.d/ntp_ampl.ntp_ampl_attack_0
```

### Create custom profiles

You can easily create custom profiles defining a new python class.

#### Steps

1. Includes the following attributes:

   - **count**: number of generated packets.
   - **interval_seconds**: between each generated packets.
   - **duration_seconds**: of the swam generation.

2. The following attributes are optional:

   - ***test**: only to test the configuration and packet creation without sending the packets.
   - **show**: summary of the generated packets,
   - **verbose**: more details about sending of the generated packets.

3. The following method is mandatory:

   - **create()**: return the packet to generated using the syntax provided by _scapy_.


[^1]: Intrusion Detection System
[^2]: Transmission Control Protocol
[^3]: Hypertext Transfer Protocol
