import json
import logging
import logging.config
import os


def setup_logging(
    default_path: str = "logging.json", default_level: int = logging.INFO, env_key: str = "LOG_CFG"
) -> None:
    """Настройка конфигурации логгирования"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
