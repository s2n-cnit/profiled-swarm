
from dynaconf import Dynaconf


def get_settings(path: str) -> Dynaconf:
    return Dynaconf(
        envvar_prefix="PROFILED_SWARM_MANAGER",
        settings_files=[path],
    )
