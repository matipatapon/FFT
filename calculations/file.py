from numpy import float64, float16, uint32, uint16, frombuffer, finfo, ndarray, complex128
from calculations.fft import FFT

def convert_float64_to_float16(x : float64) -> float16:
    if x > finfo('float16').max:
        return finfo('float16').max
    if x < finfo('float16').min:
        return finfo('float16').min
    return float16(x)

def fft_to_file(path: str, fft: FFT) -> None:
    width = uint16(fft.get_width())
    height = uint16(fft.get_height())
    f = open(path, "wb")
    f.write(width.tobytes())
    f.write(height.tobytes())

    r = fft.get_red()
    g = fft.get_green()
    b = fft.get_blue()
    z = 0
    for x in range(0, height):
        for y in range(0, width):
            for channel in (r[x][y], g[x][y], b[x][y]):
                f.write(channel.real.tobytes())
                f.write(channel.imag.tobytes())

def file_to_fft(path: str) -> FFT:
    f = open(path, "rb")
    width = int(frombuffer(f.read1(2), uint16))
    height = int(frombuffer(f.read1(2), uint16))
    print(f"width: {width}, height: {height}")

    r = ndarray(shape=(height, width), dtype=complex128)
    g = ndarray(shape=(height, width), dtype=complex128)
    b = ndarray(shape=(height, width), dtype=complex128)

    for x in range(0, height):
        for y in range(0, width):
            for channel in (r, g, b):
                channel[x][y] = complex(frombuffer(f.read1(8), float64), frombuffer(f.read1(8), float64))

    return FFT(r, b, g)

