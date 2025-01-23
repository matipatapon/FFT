import numpy as np
import matplotlib.pyplot as plt
from typing import Optional

class Image:
    def __init__(
            self,
            path : Optional[str] = None,
            red : Optional[np.ndarray] = None,
            blue : Optional[np.ndarray] = None,
            green : Optional[np.ndarray] = None):
        if path is not None:
            self._image = plt.imread(path)[:, :, :3]
            self._path = path
        elif red is not None and blue is not None and green is not None:
            image_y_size = len(red)
            image_x_size = len(red[0])
            image_channel_count = 3
            self._image = np.ndarray(
                (image_y_size,
                image_x_size,
                image_channel_count),
                np.uint8)

            self._image[:, :, 0] = red
            self._image[:, :, 1] = blue
            self._image[:, :, 2] = green
        else:
            raise ValueError("Missing fft or path to image !")

    def get_red_channel(self) -> np.ndarray:
        return self._image[:, :, 0]

    def get_blue_channel(self) -> np.ndarray:
        return self._image[:, :, 1]

    def get_green_channel(self) -> np.ndarray:
        return self._image[:, :, 2]

    def get_all_channels(self) -> np.ndarray:
        return self._image

    def get_path(self) -> str:
        if(self._path is None):
            raise ValueError("Path is not set")
        return self._path