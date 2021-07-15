import os
import json
import typing


class JsonConfigHandler:
    def __init__(self, config):
        self.config = config  # config file path
        self.default_dir = ""
        self.default_volume = 1.0
        self.load_and_read()

    def load_and_read(self) -> typing.List[typing.AnyStr]:
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
