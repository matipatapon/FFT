import numpy as np

class FFT:
    def __init__(
        self,
        red : np.ndarray,
        blue : np.ndarray,
        green : np.ndarray
    ):
        self._red = red
        self._blue = blue
        self._green = green

    def get_red(self) -> np.ndarray:
        return self._red

    def get_blue(self) -> np.ndarray:
        return self._blue

    def get_green(self) -> np.ndarray:
        return self._green
    
    def get_width(self) -> int:
        return len(self._green[0])
    
    def get_height(self) -> int:
        return len(self._green)
