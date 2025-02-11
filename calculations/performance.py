from PySide6 import os
from calculations.converter import Converter
from calculations.fft import FFT
from calculations.file import file_to_fft, fft_to_file
import numpy as np

from calculations.image import Image

class Performance:
    def __init__(self, image: Image, compressed_image_fft: FFT):
        self.image = image
        self.compressed_image_fft = compressed_image_fft

        self.original_size = 0
        self.encoded_size = 0


    # There should be something better
    def calculate_fft_size(self) -> None:
        compressed_file_name = "compressed_test_file.fft"

        fft_to_file(compressed_file_name, self.compressed_image_fft)

        self.original_size = os.path.getsize(self.image.get_path())
        self.encoded_size = os.path.getsize(compressed_file_name)

    def get_compression_ratio(self) -> float:
        compression_ratio = (self.encoded_size) / (self.original_size)
        return round(compression_ratio, 2)

    def get_compression_factor(self) -> float:
        compression_factor = (self.original_size) / (self.encoded_size)
        return round(compression_factor, 2)

    def get_original_size(self) -> int:
        return self.original_size

    def get_compressed_size(self) -> int:
        return self.encoded_size

    def get_mean_squared_error(self) -> np.floating:
        compressed_img: np.ndarray = (Converter.convert_fft_to_image(self.compressed_image_fft)).get_all_channels()
        return round(np.mean((self.image.get_all_channels() - compressed_img)**2), 2)
