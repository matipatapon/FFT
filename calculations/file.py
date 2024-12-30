import numpy as np
from calculations.fft import FFT

def fft_to_file(path: str, fft: FFT) -> None:
    width = np.uint16(fft.get_width())
    height = np.uint16(fft.get_height())
    f = open(path, "wb")
    f.write(width.tobytes())
    f.write(height.tobytes())

    red = fft.get_complex_red()
    green = fft.get_complex_green()
    blue = fft.get_complex_blue()
    how_many_zeroes_ahead = 0

    for x in range(0, height):
        for y in range(0, width):
            for channel in (red[x][y], green[x][y], blue[x][y]):
                if channel == 0 and how_many_zeroes_ahead != np.iinfo('uint8').max and (x != height -1 and y != width -1):
                    how_many_zeroes_ahead+=1
                    continue
                f.write(np.uint8(how_many_zeroes_ahead).tobytes())
                how_many_zeroes_ahead = 0
                f.write(channel.tobytes())

def file_to_fft(path: str) -> FFT:
    f = open(path, "rb")

    width = np.frombuffer(f.read1(2), np.uint16, 1)[0]
    height = np.frombuffer(f.read1(2), np.uint16, 1)[0]
    red = np.ndarray(shape=(height, width), dtype=np.complex128)
    green = np.ndarray(shape=(height, width), dtype=np.complex128)
    blue = np.ndarray(shape=(height, width), dtype=np.complex128)
    how_many_zeroes_ahead = 0
    how_many_zeroes_ahead_readed = False

    for x in range(0, height):
        for y in range(0, width):
            for channel in (red, green, blue):
                if not how_many_zeroes_ahead_readed:
                    how_many_zeroes_ahead = np.frombuffer(f.read1(1), np.uint8, 1)[0]
                    how_many_zeroes_ahead_readed = True
                if how_many_zeroes_ahead != 0:
                    channel[x][y] = np.complex128(0, 0)
                    how_many_zeroes_ahead-=1
                    continue
                channel[x][y] = np.frombuffer(f.read1(16), np.complex128, 1)[0]
                how_many_zeroes_ahead_readed = False

    return FFT(red, green, blue)
