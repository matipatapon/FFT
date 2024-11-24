import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
#https://homepages.inf.ed.ac.uk/rbf/HIPR2/fourier.htm
image_filename = "test.bmp"

class Image:
    def __init__(self, path : Optional[str] = None, fft : Optional["FFT"] = None):
        if path != None:
            self._image = plt.imread(path)
        elif fft != None:
            image_y_size = len(fft.get_red())
            image_x_size = len(fft.get_red()[0])
            image_channel_count = 3
            self._image = np.ndarray(
                (image_y_size,
                image_x_size,
                image_channel_count),
                np.uint8)

            self._image[:, :, 0] = self._fft_to_channel(fft.get_red())
            self._image[:, :, 1] = self._fft_to_channel(fft.get_blue())
            self._image[:, :, 2] = self._fft_to_channel(fft.get_green())
        else:
            raise ValueError("Missing fft or path to image !")

    def get_red_channel(self) -> np.ndarray:
        return self._image[:, :, 0]

    def get_blue_channel(self) -> np.ndarray:
        return self._image[:, :, 1]

    def get_green_channel(self) -> np.ndarray:
        return self._image[:, :, 2]

    def get_all_channels(self) -> np.ndarray:
        return self._image

    def _fft_to_channel(self, fft : np.ndarray) -> np.ndarray:
        return abs(np.fft.ifft2(fft))

class FFT:
    def __init__(self, image : Image):
        self._red_fft = self._channel_to_fft(image.get_red_channel())
        self._blue_fft = self._channel_to_fft(image.get_blue_channel())
        self._green_fft = self._channel_to_fft(image.get_green_channel())

    def get_red(self):
        return self._red_fft

    def get_blue(self):
        return self._blue_fft

    def get_green(self):
        return self._green_fft

    def _channel_to_fft(self, channel : np.ndarray) -> np.ndarray:
        return np.fft.fftshift(np.fft.fft2(channel))

image = Image(path=image_filename)

plt.subplot(632)
plt.tight_layout()
plt.title("Orginal image")
plt.axis("off")
plt.imshow(image.get_all_channels())

plt.set_cmap("gray")
plt.subplot(634)
plt.title("Red channel")
plt.axis("off")
plt.imshow(image.get_red_channel())

plt.subplot(635)
plt.title("Blue channel")
plt.axis("off")
plt.imshow(image.get_blue_channel())

plt.subplot(636)
plt.title("Green channel")
plt.axis("off")
plt.imshow(image.get_green_channel())

fft = FFT(image)

plt.set_cmap("gray")
plt.subplot(637)
plt.title("FFT of red channel")
plt.axis("off")
plt.imshow(np.log(abs(fft.get_red())))

plt.subplot(638)
plt.title("FFT of blue channel")
plt.axis("off")
plt.imshow(np.log(abs(fft.get_blue())))

plt.subplot(639)
plt.title("FFT of green channel")
plt.axis("off")
plt.imshow(np.log(abs(fft.get_green())))

reconstructed_image = Image(fft=fft)

plt.subplot(6, 3, 10)
plt.title("Recreated red channel")
plt.axis("off")
plt.imshow(reconstructed_image.get_red_channel())

plt.subplot(6, 3, 11)
plt.title("Recreated blue channel")
plt.axis("off")
plt.imshow(reconstructed_image.get_blue_channel())

plt.subplot(6, 3, 12)
plt.title("Recreated green channel")
plt.axis("off")
plt.imshow(reconstructed_image.get_green_channel())

plt.subplot(6,3,14)
plt.title("Recreated image")
plt.axis("off")
plt.imshow(reconstructed_image.get_all_channels())
plt.set_cmap("viridis")

plt.show()
#https://homepages.inf.ed.ac.uk/rbf/HIPR2/fourier.htm