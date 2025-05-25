from fabric.api import cd, run

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
