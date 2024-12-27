import numpy as np
from calculations.fft import FFT

def fft_to_file(path: str, fft: FFT) -> None:
    width = np.uint16(fft.get_width())
    height = np.uint16(fft.get_height())
    f = open(path, "wb")
    f.write(width.tobytes())
    f.write(height.tobytes())

    red = fft.get_red()
    green = fft.get_green()
    blue = fft.get_blue()
    z = np.uint8(0)

    for x in range(0, height):
        for y in range(0, width):
            for channel in (red[x][y], green[x][y], blue[x][y]):
                if channel == 0 and z != np.iinfo('uint8').max and (x != height - 1 or y != width - 1):
                    z+=1
                    continue
                f.write(channel.real.tobytes())
                f.write(channel.imag.tobytes())
                f.write(z.tobytes())
                z = np.uint8(0)

def file_to_fft(path: str) -> FFT:
    f = open(path, "rb")
    width = int(np.frombuffer(f.read1(2), np.uint16))
    height = int(np.frombuffer(f.read1(2), np.uint16))

    r = np.ndarray(shape=(height, width), dtype=np.complex128)
    g = np.ndarray(shape=(height, width), dtype=np.complex128)
    b = np.ndarray(shape=(height, width), dtype=np.complex128)
    skip = 0
    for x in range(0, height):
        for y in range(0, width):
            for channel in (r, g, b):
                if skip != 0:
                    channel[x][y] = np.complex128(0,0)
                    skip-=1
                    continue
                channel[x][y] = np.complex128(np.frombuffer(f.read1(8), np.float64, 1), np.frombuffer(f.read1(8), np.float64, 1))
                skip = np.frombuffer(f.read1(1), np.uint8, 1)[0]
                print(skip)

    return FFT(r, b, g)
