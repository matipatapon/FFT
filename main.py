import numpy as np
import matplotlib.pyplot as plt
from image import Image
from fft import FFT
from converter import Converter

image_filename = "test.bmp"

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

fft = Converter.convert_image_to_fft(image)

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

reconstructed_image = Converter.convert_fft_to_image(fft)

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
