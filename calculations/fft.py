import numpy as np

class FFT:
    def __init__(
        self,
        red : np.ndarray,
        blue : np.ndarray,
        green : np.ndarray
    ):
        self._red = red
        self._blue = blue
        self._green = green

    def get_red(self) -> np.ndarray:
        return self._red

    def get_blue(self) -> np.ndarray:
        return self._blue

    def get_green(self) -> np.ndarray:
        return self._green
    
    def _apply_threshold_to_fft_single_channel(fft : np.ndarray, threshold : float) -> np.ndarray: #pass data after .fft2, threshold is percentage written in decimal (ie. 10% = 0,1)
        fft_sort = np.sort(np.abs(fft.reshape(-1))) #get sorted vector with just the values for determining the numeric value of threshold
        threshold_num_val = fft_sort[int(np.floor((1 - threshold) * len(fft_sort)))] #get numeric value from the vector
        mask = np.abs(fft) > threshold_num_val #make 0 and 1 mask using the numeric value
        threshold_fft = fft * mask #mask the values to be truncated
        return threshold_fft #return fft
    
    def apply_threshold_to_fft(fft : 'FFT', threshold : float) -> 'FFT': #For each channel's fft run the thresholding method and return FFT object with the results
        return FFT(
            FFT._apply_threshold_to_fft_single_channel(fft.get_red(), threshold),
            FFT._apply_threshold_to_fft_single_channel(fft.get_blue(), threshold),
            FFT._apply_threshold_to_fft_single_channel(fft.get_green(), threshold)
        )

