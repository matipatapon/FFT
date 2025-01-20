import numpy as np
from calculations.image import Image
from calculations.converter import Converter
from calculations.fft import FFT
from settings import *
from gui.Gui import Gui
from typing import Optional
from calculations.file import file_to_fft, fft_to_file
from calculations.performance import Performance
from time import time

class Controller:
    def __init__(self, gui: Gui):
        self._image: Optional[Image] = None
        self._gui: Gui = gui
        self.compressed_fft: Optional[FFT] = None
        self.compression_time = 0

    def refreshFFT(self, threshold: float):
        if self._image:
            t1 = time() 
            fft = FFT.from_image(self._image, threshold)
            t2 = time()
            self.compression_time = t2 - t1

            self.compressed_fft = fft

            self._gui.add_image_to_plot(np.log(abs(fft.get_complex_red())), 3, "FFT of red channel", GRAY)
            self._gui.add_image_to_plot(np.log(abs(fft.get_complex_blue())), 4, "FFT of blue channel", GRAY)
            self._gui.add_image_to_plot(np.log(abs(fft.get_complex_green())), 5, "FFT of green channel", GRAY)

            reconstructed_image: Image = Converter.convert_fft_to_image(fft)
            self._gui.setRecreatedImage(reconstructed_image.get_all_channels(), "Recreated image")
            self._gui.add_image_to_plot(reconstructed_image.get_red_channel(), 6, "Recreated red channel", GRAY)
            self._gui.add_image_to_plot(reconstructed_image.get_blue_channel(), 7, "Recreated blue channel", GRAY)
            self._gui.add_image_to_plot(reconstructed_image.get_green_channel(), 8, "Recreated green channel", GRAY)

            self._gui.add_compressed_image_to_stats(reconstructed_image.get_all_channels())

    def changeFFTFile(self, path: str) -> None:
        fft = file_to_fft(path)
        self._image = Converter.convert_fft_to_image(fft)

        self._gui.add_image_to_plot(self._image.get_red_channel(), 0, "Red channel", GRAY)
        self._gui.add_image_to_plot(self._image.get_blue_channel(), 1, "Blue channel", GRAY)
        self._gui.add_image_to_plot(self._image.get_green_channel(), 2, "Green channel", GRAY)

        self._gui.add_image_to_drop_label(self._image.get_all_channels())

        self.refreshFFT(0.1)

    def changeFile(self, path: str) -> None:
        self._image = Image(path)

        self._gui.add_image_to_plot(self._image.get_red_channel(), 0, "Red channel", GRAY)
        self._gui.add_image_to_plot(self._image.get_blue_channel(), 1, "Blue channel", GRAY)
        self._gui.add_image_to_plot(self._image.get_green_channel(), 2, "Green channel", GRAY)

        self.refreshFFT(0.1)

    def saveFile(self, path: str) -> None:
        if self.compressed_fft: 
            fft_to_file(path, self.compressed_fft)

    def calculateCompressionStatistics(self) -> None:
        if self._image is None:
            return 
        performance = Performance(FFT.from_image(self._image,1), self.compressed_fft)
        performance.calculate_fft_size()

        stats = [
            f"Original Image Size: {performance.get_original_size()}",
            f"Compressed Image Size: {performance.get_compressed_size()}",
            f"Compression Time : {round(self.compression_time,4)}",
            f"Compression Ratio: {performance.get_compression_ratio()}",
            f"Compression Factor: {performance.get_compression_factor()}",
            f"Mean Squared Error: {performance.get_mean_squared_error()}"
        ]
        self._gui.setStatistics(stats)
