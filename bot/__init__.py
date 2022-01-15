import yaml

from .image import ImageReader

with open("settings.yaml", "r") as stream:
    settings = yaml.safe_load(stream)


image_reader = ImageReader(settings["RESOURCES_DIR"], settings["ZOOM"])