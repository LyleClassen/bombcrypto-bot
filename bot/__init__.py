import yaml

from .image import ImageReader

with open("settings.yaml", "r") as stream:
    settings = yaml.safe_load(stream)


image_reader = ImageReader(settings["resources_dir"], settings["zoom"])