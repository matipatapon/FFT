import numpy as np
from calculations.image import Image
from calculations.converter import Converter
from calculations.fft import FFT
from settings import *
from gui.Gui import Gui

class Controller:
    def __init__(self, gui: Gui):
        self.fft: FFT | None = None 
        self.path: str = ""
        self.gui: Gui = gui

    def changeThreshold(self, value: float) -> None:
        if self.fft:
            fft: FFT = FFT.apply_threshold_to_fft(self.fft, value)
            reconstructed_image: Image = Converter.convert_fft_to_image(fft)
            self.gui.setRecreatedImage(reconstructed_image.get_all_channels(), "Recreated image")

    def changeFile(self, path: str) -> None:
        self.path = path
        image: Image = Image(path)

        self.gui.add_image_to_plot(image.get_red_channel(), 0, "Red channel", GRAY)
        self.gui.add_image_to_plot(image.get_blue_channel(), 1, "Blue channel", GRAY)
        self.gui.add_image_to_plot(image.get_green_channel(), 2, "Green channel", GRAY)

        fft: FFT = Converter.convert_image_to_fft(image)
        self.fft = fft

        self.gui.add_image_to_plot(np.log(abs(fft.get_red())), 3, "FFT of red channel", GRAY)
        self.gui.add_image_to_plot(np.log(abs(fft.get_blue())), 4, "FFT of blue channel", GRAY)
        self.gui.add_image_to_plot(np.log(abs(fft.get_green())), 5, "FFT of green channel", GRAY)

        fft = FFT.apply_threshold_to_fft(fft, 0.1)
        reconstructed_image = Converter.convert_fft_to_image(fft)

        # Maybe add it later ?
        # add_image_to_plot(reconstructed_image.get_red_channel(), 10, "Recreated red channel", GRAY)
        # add_image_to_plot(reconstructed_image.get_blue_channel(), 11, "Recreated blue channel", GRAY)
        # add_image_to_plot(reconstructed_image.get_green_channel(), 12, "Recreated green channel", GRAY)
        # self.gui.set(reconstructed_image.get_all_channels(), 14, "Recreated image", COLOR)
        self.gui.setRecreatedImage(reconstructed_image.get_all_channels(), "Recreated image")
