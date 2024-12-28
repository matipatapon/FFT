import numpy as np
from calculations.fft import FFT

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

def _int16_to_float64(int16: np.int16):
    int32 = np.int32(int16)
    int32 <<= 16
    return np.float64(int32)

def fft_to_file(path: str, fft: FFT) -> None:
    width = np.uint16(fft.get_width())
    height = np.uint16(fft.get_height())
    f = open(path, "wb")
    f.write(width.tobytes())
    f.write(height.tobytes())

    red = fft.get_red()
    green = fft.get_green()
    blue = fft.get_blue()
    how_many_zeroes_ahead = 0

    for x in range(0, height):
        for y in range(0, width):
            for channel in (red[x][y], green[x][y], blue[x][y]):
                if channel == 0 and how_many_zeroes_ahead != np.iinfo('uint8').max and (x != height - 1 or y != width - 1):
                    how_many_zeroes_ahead+=1
                    continue
                f.write(_float64_to_int16(channel.real).tobytes())
                f.write(_float64_to_int16(channel.imag).tobytes())
                f.write(np.uint8(how_many_zeroes_ahead).tobytes())
                how_many_zeroes_ahead = 0

def file_to_fft(path: str) -> FFT:
    f = open(path, "rb")

    width = np.frombuffer(f.read1(2), np.uint16, 1)[0]
    height = np.frombuffer(f.read1(2), np.uint16, 1)[0]
    red = np.ndarray(shape=(height, width), dtype=np.complex128)
    green = np.ndarray(shape=(height, width), dtype=np.complex128)
    blue = np.ndarray(shape=(height, width), dtype=np.complex128)
    how_many_zeroes_ahead = 0

    for x in range(0, height):
        for y in range(0, width):
            for channel in (red, green, blue):
                if how_many_zeroes_ahead != 0:
                    channel[x][y] = np.complex128(0, 0)
                    how_many_zeroes_ahead-=1
                    continue
                real = _int16_to_float64(np.frombuffer(f.read1(2), np.int16, 1)[0])
                imag = _int16_to_float64(np.frombuffer(f.read1(2), np.int16, 1)[0])
                channel[x][y] = np.complex128(real, imag)
                how_many_zeroes_ahead = np.frombuffer(f.read1(1), np.uint8, 1)[0]

    BROKEN :(

    return FFT(red, green, blue)
