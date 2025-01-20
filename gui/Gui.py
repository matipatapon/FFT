from PySide6.QtWidgets import QMainWindow
from gui.MenuTabs import MenuTabs
from gui.PrimaryWindow import PrimaryWindow
from gui.RecreatedImagesWindow import RecreatedImagesWindow
from gui.StatsWindow import StatsWindow
from gui.InformationWindow import InformationWindow
from PySide6.QtCore import Signal
import numpy as np

class Gui(QMainWindow):
    fileChangedSignal = Signal(str)
    saveFileSignal = Signal(str)
    fftFileChangedSignal = Signal(str)
    thresholdChangedSignal = Signal(float)
    calculateStatisticsSignal = Signal()

    def __init__(self):
        super().__init__()

        self.menu = MenuTabs()
        self.menu.setStyleSheet("background-color: #272c36")
        self.setStyleSheet("background-color: #272c36")

        self.primaryWindow = PrimaryWindow()
        self.primaryWindow.fileDroppedSignal.connect(self.pathChanged)
        self.primaryWindow.fftFileSelectedSignal.connect(self.fftPathChanged)
        self.primaryWindow.saveFileSignal.connect(self.saveFile)
        self.primaryWindow.slider.sliderValueChanged.connect(self.thresholdChanged)

        self.recreatedImagesWindow = RecreatedImagesWindow()

        self.statsWindow = StatsWindow()
        self.statsWindow.getStatisticsSignal.connect(self.getStatistics)

        self.informationWindow = InformationWindow()

        self.menu.addWidget(self.primaryWindow, "Image")
        self.menu.addWidget(self.recreatedImagesWindow, "Plots")
        self.menu.addWidget(self.statsWindow, "Statistics")
        self.menu.addWidget(self.informationWindow, "Information")

        self.setCentralWidget(self.menu)


    def add_image_to_plot(
    self,
    ndarray : np.ndarray,
    position : int,
    title : str,
    color : bool) -> None:
        self.recreatedImagesWindow.add_image_to_plot(ndarray, position, title, color)


    def add_image_to_drop_label(self,ndarray : np.ndarray) -> None:
        self.primaryWindow.setFFTImage(ndarray)

    def setRecreatedImage(self, ndArray: np.ndarray, title: str) -> None:
        self.primaryWindow.setRecreatedImage(ndArray, title)

    def pathChanged(self, filePath: str) -> None:
        self.fileChangedSignal.emit(filePath)

    def fftPathChanged(self, filePath: str) -> None:
        self.fftFileChangedSignal.emit(filePath)

    def thresholdChanged(self, value: float) -> None:
        self.thresholdChangedSignal.emit(value)

    def saveFile(self, filePath: str) -> None:
        self.saveFileSignal.emit(filePath)

    def getStatistics(self) -> None:
        self.calculateStatisticsSignal.emit()

    def setStatistics(self, statistics: list[str]) -> None:
        self.statsWindow.setStatistics(statistics)

    def add_compressed_image_to_stats(self, ndarray: np.ndarray) -> None:
        self.statsWindow.add_compressed_image(ndarray)
