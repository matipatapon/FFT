import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

image_filename = "test.bmp"

class ImageToFFTConverter:
    def _to_fft(self, channel : np.ndarray) -> np.ndarray:
        return np.fft.fftshift(np.fft.fft2(channel))

    def __init__(self, image : np.ndarray) -> None:
        self.red_fft = self._to_fft(image[:, :, 0])
        self.blue_fft = self._to_fft(image[:, :, 1])
        self.green_fft = self._to_fft(image[:, :, 2])

class FFTToImageConverter:
    def _to_channel(self, fft : np.ndarray) -> np.ndarray:
        return np.fft.ifft2(fft)

    def _channels_to_image(self) -> np.ndarray:
        image_y_size = len(self.red_channel)
        image_x_size = len(self.red_channel[0])
        image_channel_count = 3
        image = np.ndarray(
            (image_y_size,
             image_x_size,
             image_channel_count),
             np.uint8)
        
        image[:, :, 0] = abs(self.red_channel)
        image[:, :, 1] = abs(self.blue_channel)
        image[:, :, 2] = abs(self.green_channel)
        return image

    def __init__(
            self,
            red : np.ndarray,
            blue : np.ndarray,
            green : np.ndarray
    ) -> None:
        self.red_channel = self._to_channel(red)
        self.blue_channel = self._to_channel(blue)
        self.green_channel = self._to_channel(green)
        self.image = self._channels_to_image()

image = plt.imread(image_filename)

plt.subplot(532)
plt.tight_layout()
plt.title("Orginal image")
plt.axis("off")
plt.imshow(image)
img_to_fft_conv = ImageToFFTConverter(image)

plt.set_cmap("gray")
plt.subplot(534)
plt.title("FFT of red channel")
plt.axis("off")
plt.imshow(np.log(abs(img_to_fft_conv.red_fft)))

plt.subplot(535)
plt.title("FFT of blue channel")
plt.axis("off")
plt.imshow(np.log(abs(img_to_fft_conv.blue_fft)))

plt.subplot(536)
plt.title("FFT of green channel")
plt.axis("off")
plt.imshow(np.log(abs(img_to_fft_conv.green_fft)))

fft_to_img_conv = FFTToImageConverter(
    img_to_fft_conv.red_fft,
    img_to_fft_conv.blue_fft,
    img_to_fft_conv.green_fft)

plt.subplot(537)
plt.title("Red channel from FFT")
plt.axis("off")
plt.imshow(abs(fft_to_img_conv.red_channel))

plt.subplot(538)
plt.title("Blue channel from FFT")
plt.axis("off")
plt.imshow(abs(fft_to_img_conv.blue_channel))

plt.subplot(539)
plt.title("Green channel from FFT")
plt.axis("off")
plt.imshow(abs(fft_to_img_conv.green_channel))

plt.subplot(5,3,11)
plt.title("Recreated image")
plt.axis("off")
plt.imshow(abs(fft_to_img_conv.image))
plt.set_cmap("viridis")

plt.show()
