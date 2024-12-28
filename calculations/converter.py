from calculations.image import Image
from calculations.fft import FFT
import numpy as np

class Converter:
    def convert_fft_to_image(fft : FFT) -> Image:
        return Image(
            red=Converter._fft_to_channel(fft.get_red()),
            blue=Converter._fft_to_channel(fft.get_blue()),
            green=Converter._fft_to_channel(fft.get_green())
        )

    def _fft_to_channel(fft : np.ndarray) -> np.ndarray:
        return abs(np.fft.ifft2(fft))
