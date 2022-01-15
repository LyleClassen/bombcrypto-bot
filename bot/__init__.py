import os

import yaml

with open("settings.yaml", "r") as stream:
    settings = yaml.safe_load(stream)


def resource_path(filename: str) -> str:
    return os.path.join(settings["RESOURCES_DIR"], filename)
