import os
from typing import Any

import yaml


class Config:
    def __init__(self, config_path: str) -> None:
        """Initialize config object.

        Args:
            config_path: Path to config file.
        """
        config = self.parse(config_path)

        self.TOKEN = os.environ.get("TOKEN", config["TOKEN"])
        self.couples_delta = int(os.environ.get("COUPLES_DELTA", config["couples_delta"]))
        self.groups = config["groups"]

        self.database_file = os.environ.get("DATABASE_FILE", "database.db")
        self.log_file = os.environ.get("LOG_FILE", "app.log")

    def parse(self, config_path: str) -> dict[str, Any]:
        """Parse config file.

        Args:
            config_path: Path to config file.

        Returns:
            Config dict.
        """
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
        return config


config = Config(os.environ.get("CONFIG_PATH", "app/config.yaml"))
