import os
import cv2
import numpy as np


class ImageReader(object):
    def __init__(self, resource_dir: str = "resources", zoom: float = 1.0):
        self.resource_dir = resource_dir
        self.zoom = zoom

    def resize(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, (0, 0), fx=self.zoom, fy=self.zoom)

    def resource_path(self, filename: str) -> str:
        return os.path.join(self.resource_dir, filename)

    def read(self, filename: str) -> np.ndarray:
        return self.resize(cv2.imread(self.resource_path(filename)))