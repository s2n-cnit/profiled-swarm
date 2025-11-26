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

Profiled Swarm uses _Poetry_ for dependency management, which is the recommended way to install and run the project in an isolated Python environment.

## Prerequisites

1. You must have _Python 3.8+ installed.
2. You need Poetry. If you do not have it, install it globally using pip install poetry.

## Setup Steps

1. **Clone the Repository**: begin by cloning the project files to your local machine:

```shell
git clone [https://github.com/s2n-cnit/profiled-swarm.git](https://github.com/s2n-cnit/profiled-swarm.git)
cd profiled-swarm
```

2. **Install Dependencies**: use Poetry to read the configuration file (_pyproject.toml_) and install all necessary dependencies, including core libraries like Scapy for packet crafting.

```shell
poetry install
```

3. **Activate the Environment**: the isolated virtual environment provided by Poetry.

```shell
poetry shell
```

## Basic Usage

The primary entry point is the _profiled-swarm.py_ script, which is controlled by a main configuration file, typically named manager.toml.ù

TODO...
