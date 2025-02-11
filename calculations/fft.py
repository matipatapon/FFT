import numpy as np
from calculations.image import Image
class FFT:
    def __init__(
        self,
        red : np.ndarray,
        green : np.ndarray,
        blue : np.ndarray,
    ):
        self._red =  red
        self._green = green
        self._blue = blue

    def from_image(img: Image, threshold: float):
        red_channel = FFT._apply_threshold_to_fft_single_channel(
            FFT._channel_to_fft(img.get_red_channel()), threshold
        )
        green_channel = FFT._apply_threshold_to_fft_single_channel(
            FFT._channel_to_fft(img.get_green_channel()), threshold
        )
        blue_channel = FFT._apply_threshold_to_fft_single_channel(
            FFT._channel_to_fft(img.get_blue_channel()), threshold
        )

        return FFT(
            red_channel,
            green_channel,
            blue_channel)

    def _apply_threshold_to_fft_single_channel(fft : np.ndarray, threshold : float) -> np.ndarray: #pass data after .fft2, threshold is percentage written in decimal (ie. 10% = 0,1)
        fft_sort = np.sort(np.abs(fft.reshape(-1))) #get sorted vector with just the values for determining the numeric value of threshold
        threshold_num_val = fft_sort[int(np.floor((1 - threshold) * len(fft_sort)))] #get numeric value from the vector
        mask = np.abs(fft) > threshold_num_val #make 0 and 1 mask using the numeric value
        threshold_fft = fft * mask #mask the values to be truncated
        return threshold_fft #return fft

    def _channel_to_fft(channel : np.ndarray) -> np.ndarray:
        return np.fft.fftshift(np.fft.fft2(channel))

    def get_width(self) -> int:
        return len(self._red[0])
    
    def get_height(self) -> int:
        return len(self._red)

    def get_complex_red(self) -> np.ndarray:
        return self._red

    def get_complex_green(self) -> np.ndarray:
        return self._green

    def get_complex_blue(self) -> np.ndarray:
        return self._blue
