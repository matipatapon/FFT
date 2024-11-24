from image import Image
from fft import FFT
import numpy as np

class Converter:
    def convert_image_to_fft(img : Image) -> FFT:
        return FFT(
            Converter._channel_to_fft(img.get_red_channel()),
            Converter._channel_to_fft(img.get_blue_channel()),
            Converter._channel_to_fft(img.get_green_channel())
        )

    def convert_fft_to_image(fft : FFT) -> Image:
        return Image(
            red=Converter._fft_to_channel(fft.get_red()),
            blue=Converter._fft_to_channel(fft.get_blue()),
            green=Converter._fft_to_channel(fft.get_green())
        )

    def _channel_to_fft(channel : np.ndarray) -> np.ndarray:
        return np.fft.fftshift(np.fft.fft2(channel))

    def _fft_to_channel(fft : np.ndarray) -> np.ndarray:
        return abs(np.fft.ifft2(fft))
