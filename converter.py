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
    
    def _apply_threshold_to_fft_single_channel(fft : np.ndarray, threshold : float) -> np.ndarray: #pass data after .fft2, threshold is percentage written in decimal (ie. 10% = 0,1)
        fft_sort = np.sort(np.abs(fft.reshape(-1))) #get sorted vector with just the values for determining the numeric value of threshold
        threshold_num_val = fft_sort[int(np.floor((1 - threshold) * len(fft_sort)))] #get numeric value from the vector
        mask = np.abs(fft) > threshold_num_val #make 0 and 1 mask using the numeric value
        threshold_fft = fft * mask #mask the values to be truncated
        return threshold_fft #return fft
    
    def apply_threshold_to_fft(fft : FFT) -> FFT: #For each channel's fft run the thresholding method and return FFT object with the results
        return FFT(
            Converter._apply_threshold_to_fft_single_channel(fft.get_red),
            Converter._apply_threshold_to_fft_single_channel(fft.get_green),
            Converter._apply_threshold_to_fft_single_channel(fft.get_blue)
        )