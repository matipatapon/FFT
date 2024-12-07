from PySide6.QtWidgets import QMainWindow
from gui.MenuTabs import MenuTabs
from gui.PrimaryWindow import PrimaryWindow
from PySide6.QtCore import Signal
import numpy as np

class Gui(QMainWindow):
    fileChangedSignal = Signal(str)
    thresholdChangedSignal = Signal(float)

    def __init__(self):
        super().__init__()

        self.menu = MenuTabs()
        self.menu.show()

        self.primaryWindow = PrimaryWindow()
        self.primaryWindow.topWindow.fileDroppedSignal.connect(self.pathChanged)
        self.primaryWindow.bottomWindow.slider.sliderValueChanged.connect(self.thresholdChanged)

        self.menu.addWidget(self.primaryWindow, "FFT")

        self.setCentralWidget(self.menu)

    def add_image_to_plot(
    self,
    ndarray : np.ndarray,
    position : int,
    title : str,
    color : bool):
        self.primaryWindow.setPlots(ndarray, position, title, color)

    def setRecreatedImage(self, ndArray: np.ndarray, title: str):
        self.primaryWindow.setRecreatedImage(ndArray, title)

    def pathChanged(self, filePath):
        self.fileChangedSignal.emit(filePath)

    def thresholdChanged(self, value):
        self.thresholdChangedSignal.emit(value)

