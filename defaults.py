import json
import os
import typing


class JsonConfigHandler:
    """JSON Management class"""

    def __init__(self, config: str):
        self.config = config  # config file path
        self.default_dir = ""
        self.default_volume = 1.0
        self.load_and_read()

    def load_and_read(self) -> typing.List[typing.AnyStr]:
        """Loads and parses a JSON"""
        f = json.load(
            open(
                f"{self.config}",
            )
        )
        if "default-dir" == "" or not os.path.exists(f["default-dir"]):
            self.default_dir == os.getcwd()
        else:
            self.default_dir = f["default-dir"]

        self.default_volume = f["default-volume"]
        return
