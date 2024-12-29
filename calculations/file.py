import numpy as np
from calculations.fft import FFT

def fft_to_file(path: str, fft: FFT) -> None:
    width = np.uint16(fft.get_width())
    height = np.uint16(fft.get_height())
    f = open(path, "wb")
    f.write(width.tobytes())
    f.write(height.tobytes())

    red_real = fft.get_int_red_real()
    red_imag = fft.get_int_red_imag()
    green_real = fft.get_int_green_real()
    green_imag = fft.get_int_green_imag()
    blue_real = fft.get_int_blue_real()
    blue_imag = fft.get_int_blue_imag()
    how_many_zeroes_ahead = 0

    for x in range(0, height):
        for y in range(0, width):
            for channel in (red_real[x][y],
                            red_imag[x][y],
                            green_real[x][y],
                            green_imag[x][y],
                            blue_real[x][y],
                            blue_imag[x][y]):
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
    red_real = np.ndarray(shape=(height, width), dtype=np.int16)
    red_imag = np.ndarray(shape=(height, width), dtype=np.int16)
    green_real = np.ndarray(shape=(height, width), dtype=np.int16)
    green_imag = np.ndarray(shape=(height, width), dtype=np.int16)
    blue_real = np.ndarray(shape=(height, width), dtype=np.int16)
    blue_imag = np.ndarray(shape=(height, width), dtype=np.int16)
    how_many_zeroes_ahead = 0
    how_many_zeroes_ahead_readed = False

    for x in range(0, height):
        for y in range(0, width):
            for channel in (red_real, red_imag, green_real, green_imag, blue_real, blue_imag):
                if not how_many_zeroes_ahead_readed:
                    how_many_zeroes_ahead = np.frombuffer(f.read1(1), np.uint8, 1)[0]
                    how_many_zeroes_ahead_readed = True
                if how_many_zeroes_ahead != 0:
                    channel[x][y] = np.int16(0)
                    how_many_zeroes_ahead-=1
                    continue
                channel[x][y] = np.frombuffer(f.read1(2), np.int16, 1)[0]
                how_many_zeroes_ahead_readed = False

    return FFT(red_real, red_imag, green_real, green_imag, blue_real, blue_imag)
