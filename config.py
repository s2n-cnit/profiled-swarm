
from dynaconf import Dynaconf


def get_settings(path: str) -> Dynaconf:
    return Dynaconf(
        envvar_prefix="HTTP_GENERATOR",
        settings_files=['settings.toml'],
    )
