import numpy as np
from calculations.image import Image
class FFT:
    def __init__(
        self,
        red_real : np.ndarray,
        red_imag : np.ndarray,
        green_real : np.ndarray,
        green_imag : np.ndarray,
        blue_real : np.ndarray,
        blue_imag : np.ndarray,
    ):
        self._red_real = red_real
        self._red_imag = red_imag
        self._red_complex =  FFT._convert_to_complex_array(self._red_real, self._red_imag)
        self._green_real = green_real
        self._green_imag = green_imag
        self._green_complex = FFT._convert_to_complex_array(self._green_real, self._green_imag)
        self._blue_real = blue_real
        self._blue_imag = blue_imag
        self._blue_complex = FFT._convert_to_complex_array(self._blue_real, self._blue_imag)

    def _convert_to_complex_array(real_array: np.ndarray, imag_array: np.ndarray):
        width = len(real_array[0])
        height = len(real_array)
        complex_array = np.ndarray([height, width], np.complex128)
        for x in range(0, height):
            for y in range(0, width):
                complex_array[x][y] = np.complex128(
                    FFT._int16_to_float64(
                        real_array[x][y]),
                    FFT._int16_to_float64(
                        imag_array[x][y]))
        return complex_array

    def _int16_to_float64(int16: np.int16):
        int32 = np.int32(int16)
        int32 <<= 16
        return np.float64(int32)

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

        width = len(red_channel[0])
        height = len(red_channel)

        red_int16_real = np.ndarray([height, width], np.int16)
        red_int16_imag = np.ndarray([height, width], np.int16)
        green_int16_real = np.ndarray([height, width], np.int16)
        green_int16_imag = np.ndarray([height, width], np.int16)
        blue_int16_real = np.ndarray([height, width], np.int16)
        blue_int16_imag = np.ndarray([height, width], np.int16)

        for x in range(0, height):
            for y in range(0, width):
                red_int16_real[x][y] = FFT._float64_to_int16(red_channel[x][y].real)
                red_int16_imag[x][y] = FFT._float64_to_int16(red_channel[x][y].imag)
                green_int16_real[x][y] = FFT._float64_to_int16(green_channel[x][y].real)
                green_int16_imag[x][y] = FFT._float64_to_int16(green_channel[x][y].imag)
                blue_int16_real[x][y] = FFT._float64_to_int16(blue_channel[x][y].real)
                blue_int16_imag[x][y] = FFT._float64_to_int16(blue_channel[x][y].imag)

        return FFT(
            red_int16_real,
            red_int16_imag,
            green_int16_real,
            green_int16_imag,
            blue_int16_real,
            blue_int16_imag)

    def _apply_threshold_to_fft_single_channel(fft : np.ndarray, threshold : float) -> np.ndarray: #pass data after .fft2, threshold is percentage written in decimal (ie. 10% = 0,1)
        fft_sort = np.sort(np.abs(fft.reshape(-1))) #get sorted vector with just the values for determining the numeric value of threshold
        threshold_num_val = fft_sort[int(np.floor((1 - threshold) * len(fft_sort)))] #get numeric value from the vector
        mask = np.abs(fft) > threshold_num_val #make 0 and 1 mask using the numeric value
        threshold_fft = fft * mask #mask the values to be truncated
        return threshold_fft #return fft

    def _channel_to_fft(channel : np.ndarray) -> np.ndarray:
        return np.fft.fftshift(np.fft.fft2(channel))

    def _float64_to_int16(flaot64: np.float64):
        roundedFloat64 = round(flaot64)
        if np.iinfo('int32').max < roundedFloat64:
            print(f"{roundedFloat64} -> {np.iinfo('int32').max}")
            roundedFloat64 = np.iinfo('int32').max
        if np.iinfo('int32').min > roundedFloat64:
            roundedFloat64 = np.iinfo('int32').min
        roundedFloat64 = np.int32(roundedFloat64)
        roundedFloat64 >>= 16
        return np.int16(roundedFloat64)

    def get_width(self) -> int:
        return len(self._red_real[0])
    
    def get_height(self) -> int:
        return len(self._red_real)

    def get_int_red_real(self) -> np.ndarray:
        return self._red_real

    def get_int_red_imag(self) -> np.ndarray:
        return self._red_imag

    def get_int_blue_real(self) -> np.ndarray:
        return self._blue_real

    def get_int_blue_imag(self) -> np.ndarray:
        return self._blue_imag

    def get_int_green_real(self) -> np.ndarray:
        return self._green_real

    def get_int_green_imag(self) -> np.ndarray:
        return self._green_imag

    def get_complex_red(self) -> np.ndarray:
        return self._red_complex

    def get_complex_green(self) -> np.ndarray:
        return self._green_complex

    def get_complex_blue(self) -> np.ndarray:
        return self._blue_complex
