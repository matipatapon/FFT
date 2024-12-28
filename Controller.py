import numpy as np
from calculations.image import Image
from calculations.converter import Converter
from calculations.fft import FFT
from settings import *
from gui.Gui import Gui
from typing import Optional
from calculations.file import

class Controller:
    def __init__(self, gui: Gui):
        self._image: Optional[Image] = None
        self._gui: Gui = gui

    def refreshFFT(self, threshold: float):
        if self._image:
            fft = FFT.from_image(self._image, threshold)

            self._gui.add_image_to_plot(np.log(abs(fft.get_red())), 3, "FFT of red channel", GRAY)
            self._gui.add_image_to_plot(np.log(abs(fft.get_blue())), 4, "FFT of blue channel", GRAY)
            self._gui.add_image_to_plot(np.log(abs(fft.get_green())), 5, "FFT of green channel", GRAY)

            reconstructed_image: Image = Converter.convert_fft_to_image(fft)
            self._gui.setRecreatedImage(reconstructed_image.get_all_channels(), "Recreated image")

    def changeFile(self, path: str) -> None:
        self._image = Image(path)

        self._gui.add_image_to_plot(self._image.get_red_channel(), 0, "Red channel", GRAY)
        self._gui.add_image_to_plot(self._image.get_blue_channel(), 1, "Blue channel", GRAY)
        self._gui.add_image_to_plot(self._image.get_green_channel(), 2, "Green channel", GRAY)

        self.refreshFFT(0.1)

        # Maybe add it later ?
        # add_image_to_plot(reconstructed_image.get_red_channel(), 10, "Recreated red channel", GRAY)
        # add_image_to_plot(reconstructed_image.get_blue_channel(), 11, "Recreated blue channel", GRAY)
        # add_image_to_plot(reconstructed_image.get_green_channel(), 12, "Recreated green channel", GRAY)
        # self._gui.set(reconstructed_image.get_all_channels(), 14, "Recreated image", COLOR)
