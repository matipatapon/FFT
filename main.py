import numpy as np
import matplotlib.pyplot as plt
from image import Image
from converter import Converter
from fft import FFT

IMAGE_FILE_NAME = "test.bmp"
PLT_ROW_COUNT = 5
PLT_COL_COUNT = 3
COLOR = True
GRAY = False

def add_image_to_plot(
        ndarray : np.ndarray,
        position : int,
        title : str,
        color : bool
) -> None:
    plt.subplot(PLT_ROW_COUNT, PLT_COL_COUNT, position)
    plt.tight_layout()
    plt.title(title)
    plt.axis("off")
    plt.imshow(ndarray)
    plt.set_cmap("viridis" if color else "gray")


image = Image(path=IMAGE_FILE_NAME)


add_image_to_plot(image.get_all_channels(), 2, "Orginal image", COLOR)
add_image_to_plot(image.get_red_channel(), 4, "Red channel", GRAY)
add_image_to_plot(image.get_blue_channel(), 5, "Blue channel", GRAY)
add_image_to_plot(image.get_green_channel(), 6, "Green channel", GRAY)

fft = Converter.convert_image_to_fft(image)

add_image_to_plot(np.log(abs(fft.get_red())), 7, "FFT of red channel", GRAY)
add_image_to_plot(np.log(abs(fft.get_blue())), 8, "FFT of blue channel", GRAY)
add_image_to_plot(np.log(abs(fft.get_green())), 9, "FFT of green channel", GRAY)

fft = FFT.apply_threshold_to_fft(fft, 0.1) #Apply threshold. Threshold percentage will come from user in the future. Threshold manually set to 10% for now.

reconstructed_image = Converter.convert_fft_to_image(fft)

add_image_to_plot(reconstructed_image.get_red_channel(), 10, "Recreated red channel", GRAY)
add_image_to_plot(reconstructed_image.get_blue_channel(), 11, "Recreated blue channel", GRAY)
add_image_to_plot(reconstructed_image.get_green_channel(), 12, "Recreated green channel", GRAY)
add_image_to_plot(reconstructed_image.get_all_channels(), 14, "Recreated image", COLOR)

plt.show()
