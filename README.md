# Profiled Swarm

> Generator of Targeted Traffic with Profiles

## Overview

**Profiled Swarm** is a powerful Python framework designed to generate targeted, realistic network traffic based on configurable behavioural profiles.

> [!NOTE]
> Its primary function is to simulate complex network environments—such as a _swarm_ of users or bots—interacting with specific network services or hosts.

> [!TIP]
> The core distinction of Profiled Swarm is its commitment to realism. Unlike simple packet-flood generators, this tool allows engineers to define complex stateful behaviors, including inter-packet timing distributions, protocol sequences
> (e.g., TCP[^1] handshakes followed by specific HTTP[^2] requests), and dynamically varying payload sizes.

This capability is essential for creating high-fidelity network simulations that accurately reflect real-world user activity, making it a critical asset in network research and security testing.

> [!IMPORTANT]
> This tool is invaluable for researchers and engineers conducting network security experiments, performance testing, IDS[^3] validation, and generating highly specific datasets for machine learning models. Furthermore, it is perfectly >
> suited for use in defensive network architectures, such as stress-testing firewall rules, evaluating load balancer efficiency under realistic load, or generating background noise to cloak anomalous traffic within a honeypot deployment.

## Key Features

### Profile-Driven Generation

> [!NOTE]
> Define custom traffic profiles (.toml or similar configuration) to model specific behaviors (e.g., web browsing, heavy file transfers, intermittent heartbeat pings).

> [!TIP]
> The profiles are the heart of the system, allowing for the precise modeling of statistical behavior. This includes specifying packet-size distributions, protocol usage over time, and crucial parameters like _think time_ (the randomized
> delay between sending subsequent packets), which dramatically enhances the realism compared to continuous stream generation.

> [!IMPORTANT]
> You can model everything from benign IoT[^4] device communications to complex coordinated scans.

### Swarm Management

> [!NOTE]
> Coordinate multiple, simultaneous traffic generators (the _swarm_) from a centralized manager.

> [!TIP]
> The management layer handles the distribution and parallel execution of different profiles across various target hosts and interfaces.

> [!IMPORTANT]
> This capability enables large-scale, high-volume simulations, allowing a single control point to launch a heterogeneous mix of traffic streams, simulating an entire
> segment of a corporate or residential network rather than just one machine.
> This is vital for distributed performance and security testing.

### Targeted Traffic

> [!NOTE]
> Easily specify target IP[^5] addresses, ports, and protocols for focused experimentation.

> [!TIP]
> The targeting mechanism supports defining streams that interact across the network stack, from Layer 3 (IP addresses and fragmentation rules) and Layer 4 (TCP/UDP[^6] ports) all the way up to application-layer protocols.

> [!IMPORTANT]
> This allows for fine-grained control, enabling tests against specific services, assessing the effectiveness of network segmentation policies, or focusing stress tests on a single, critical application port.


### Modular Design

> [!TIP]
> Built on clear components for configuration (_config.py_), profile definition (_profile.py_), packet generation (_packets.py_), and swarm control (_manager.py_).

> [!IMPORTANT]
> This separation of concerns ensures that the framework is highly extensible.
> Developers can easily integrate new protocols into the packets.py module, introduce new behavioural models by extending profile.py, or change the configuration method without affecting the core traffic generation logic.
> This makes the tool future-proof and adaptable to evolving network standards.

## Installation

> [!NOTE]
This project appears to use _poetry_ for dependency management, which is the recommended installation method.

> [!TIP]
_Poetry_ provides robust dependency resolution and environment isolation, ensuring that the project runs consistently across different machines without conflicts with other _Python_ projects.

## Prerequisites

- Python 3.8+
  The project leverages modern Python features and requires a stable 3.8 or newer environment.
- Poetry
  Install globally:

  ```shell
  pip install poetry
  ```

> [!WARNING]
> If you prefer a platform-specific installer, consult the official _Poetry_ documentation.

## Setup

1. Clone the repository:

    ```shell
    git clone [https://github.com/s2n-cnit/profiled-swarm.git](https://github.com/s2n-cnit/profiled-swarm.git)
    cd profiled-swarm
    ```

2. Install dependencies using Poetry:

    ```shell
    poetry install
    ```

> [!TIP]
> This command reads the _pyproject.toml_ file, fetches all necessary dependencies (including core libraries like Scapy for packet crafting), and installs them into a clean, isolated virtual environment.

3. Activate the virtual environment:

   ```shell
   poetry shell
   ```

    Once activated, you can execute profiled-swarm.py directly, knowing that all required packages are available and properly configured.

## Usage

The main entry point is _profiled-swarm.py_, which is controlled by configuration files (like _manager.toml_).

1. Configure the Swarm

> [!NOTE]
> Edit the manager.toml file to define the global settings, including the network interface, logging level, and the list of profiles to execute.

   The configuration file is structured into two primary sections:

   1. _[manager]_: Defines global execution parameters.
      - interface: Specifies the network adapter (e.g., eth0, wlan0) through which all traffic will be sent.
      - log_level: Sets the verbosity of the output (_DEBUG_, _INFO_, _WARNING_, etc.).
   2. _[profiles.profile_name]_: Defines individual traffic streams that constitute the swarm. Each profile is an instance of a generator with its unique target and behavioural definition.

    A typical _manager.toml_ structure includes:

    ```ini
    [manager]
    interface = "eth0"
    log_level = "INFO"

    # Profile 1: Simulates a user browsing a specific server
    [profiles.user_profile_1]
    config_file = "config/profile_web_browser.toml" # The path to the behavioral definition file
    target_host = "192.168.1.100"                   # The destination IP address for the traffic
    rate_limit_pps = 50                             # Maximum packets per second for this specific generator

    # Profile 2: Simulates a low-rate, background bot
    [profiles.bot_profile_2]
    config_file = "config/profile_heartbeat_bot.toml"
    target_host = "10.0.0.5"
    rate_limit_pps = 5
    ```

> [!IMPORTANT]
> Each config_file referenced (e.g., _profile_web_browser.toml_) must contain the detailed parameters for the statistical distributions and protocol sequence the generator should follow.

1. Run the GeneratorExecute the main script.

> [!NOTE]
> The script will initialize the Manager, load the configurations, and start the swarm of traffic generators as parallel worker processes.

    ```shell
    python profiled-swarm.py --config manager.toml.
    ```

> [!IMPORTANT]
> Upon execution, the Manager will print its status, and each running generator will log its activity, including the start time, the profile it is executing, and any errors encountered during packet transmission.

> [!TIP]
> Use the --help flag for additional command-line options:

    ```shell
    python profiled-swarm.py --help

    # Example Output:
    # usage: profiled-swarm.py [-h] [--config CONFIG_PATH]
    #
    # optional arguments:
    #   -h, --help            show this help message and exit
    #   --config CONFIG_PATH  Specify the path to the manager configuration file. (default: manager.toml)
    ```

# License

> [!NOTE]
> This project is licensed under the **MIT** License.

> [!TIP]
> See the LICENSE file for details.


[^1]: Transmission Control Protocol
[^2]: HyperText Transfer Protocol
[^3]: Intrusion Detection System
[^4]: Internet of Things
[^5]: Internet Protocol
