import numpy as np
import matplotlib.pyplot as plt
image_filename = "image.png"

def calculate_2dft(input):
    ft = np.fft.fft2(input)

    # zmienia kolejność aby najmniejsze frekwencje były najbliżej centrum
    ft = np.fft.fftshift(ft)
    return ft

def calculate_2dift(input):
    return np.fft.ifft2(input)

def split_image_into_rgb(image):
    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]
    return red, green, blue
# Read and process image
image = plt.imread(image_filename)
red, green, blue = split_image_into_rgb(image)

ftr = calculate_2dft(red)
ftg = calculate_2dft(green)
ftb = calculate_2dft(blue)

plt.set_cmap("gray")
plt.axis("off")
plt.subplot(331)
plt.imshow(red)
plt.subplot(332)
plt.imshow(green)
plt.subplot(333)
plt.imshow(blue)
plt.subplot(334)
plt.imshow(np.log(abs(ftr)))
plt.subplot(335)
plt.imshow(np.log(abs(ftg)))
plt.subplot(336)
plt.imshow(np.log(abs(ftb)))
plt.subplot(337)
plt.imshow(abs(calculate_2dift(ftr)))
plt.subplot(338)
plt.imshow(abs(calculate_2dift(ftg)))
plt.subplot(339)
plt.imshow(abs(calculate_2dift(ftb)))

#https://thepythoncodingbook.com/2021/08/30/2d-fourier-transform-in-python-and-fourier-synthesis-of-images/
#https://www.youtube.com/watch?v=KGiV_2i713I

#abs - zmiana z complex na zwykłe
#log - aby lepiej było widać :)
plt.axis("off")
plt.show()