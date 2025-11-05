# Profiled Swarm

Profiled Swarm: Generator of Targeted Traffic with ProfilesOverviewProfiled Swarm is a powerful Python framework designed to generate targeted, realistic network traffic based on configurable behavioral profiles. Its primary function is to simulate complex network environments—such as a "swarm" of users or bots—interacting with specific network services or hosts.This tool is invaluable for researchers and engineers conducting network security experiments, performance testing, intrusion detection system (IDS) validation, and generating highly specific datasets for machine learning models.Key FeaturesProfile-Driven Generation: Define custom traffic profiles (.toml or similar configuration) to model specific behaviors (e.g., web browsing, heavy file transfers, intermittent heartbeat pings).Swarm Management: Coordinate multiple, simultaneous traffic generators (the "swarm") from a centralized manager.Targeted Traffic: Easily specify target IP addresses, ports, and protocols for focused experimentation.Modular Design: Built on clear components for configuration, profile definition, packet generation, and swarm control.InstallationThis project appears to use poetry for dependency management, which is the recommended installation method.PrerequisitesPython 3.8+Poetry (install globally: pip install poetry)SetupClone the repository:git clone [https://github.com/s2n-cnit/profiled-swarm.git](https://github.com/s2n-cnit/profiled-swarm.git)
cd profiled-swarm
Install dependencies using Poetry:poetry install
Activate the virtual environment:poetry shell
UsageThe main entry point is profiled-swarm.py, which is controlled by configuration files (like manager.toml).1. Configure the SwarmEdit the manager.toml file to define the global settings, including the network interface, logging level, and the list of profiles to execute.A typical manager.toml structure includes:[manager]
interface = "eth0"
log_level = "INFO"

[profiles.user_profile_1]
config_file = "config/profile_web_browser.toml"
target_host = "192.168.1.100"
rate_limit_pps = 50

[profiles.bot_profile_2]
config_file = "config/profile_heartbeat_bot.toml"
target_host = "10.0.0.5"
rate_limit_pps = 5
2. Run the GeneratorExecute the main script. The script will initialize the Manager, load the configurations, and start the swarm of traffic generators.python profiled-swarm.py --config manager.toml
Use the --help flag for additional command-line options.LicenseThis project is licensed under the MIT License. See the LICENSE file for details.
