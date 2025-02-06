from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QWidget
import numpy as np
import settings

from gui.PlotWidget import PlotWidget
from gui.FileButton import FileButton
from gui.DropLabel import DropLabel
from gui.ThresholdSlider import ThresholdSlider
from gui.SaveButton import SaveButton

class PrimaryWindow(QWidget):
    fileDroppedSignal = Signal(str)
    fftFileSelectedSignal = Signal(str)
    saveFileSignal = Signal(str)

    def __init__(self):
        super().__init__()

        self.resizeEvent = self.onResize

        self.dropLabel = DropLabel()
        self.dropLabel.fileSelectedSignal.connect(self.selectedFileChanged)
        self.dropLabel.fftFileSelectedSignal.connect(self.selectedFFTChanged)

        self.fftImage: PlotWidget = PlotWidget()
        self.fftImage.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.fileButton = FileButton()
        self.fileButton.fileSelectedSignal.connect(self.selectedFileChanged)
        self.fileButton.fftFileSelectedSignal.connect(self.selectedFFTChanged)

        self.plotImage = PlotWidget()
        self.plotImage.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.recreatedImagePlot = self.plotImage.sc

        self.saveButton = SaveButton()
        self.saveButton.fileSavedSignal.connect(self.saveFile)

        self.slider = ThresholdSlider()

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)

        orignalImgLabel = self.createImageLabel()
        orignalImgLabel.setText("Original Image")
        compressedImgLabel= self.createImageLabel()
        compressedImgLabel.setText("Compressed Image")

        self.gridLayout.addWidget(orignalImgLabel, 0, 0)
        self.gridLayout.addWidget(compressedImgLabel, 0, 1)

        self.gridLayout.addWidget(self.dropLabel, 1, 0)
        self.gridLayout.addWidget(self.recreatedImagePlot, 1, 1)

        self.gridLayout.addWidget(self.fileButton, 2, 0 )
        self.gridLayout.addWidget(self.saveButton, 2, 1)
        self.gridLayout.addWidget(self.slider, 1, 3 )

        self.gridLayout.setRowStretch(1,6)
        self.gridLayout.setColumnStretch(0,6)
        self.gridLayout.setColumnStretch(1,6)

        holderWidget = QWidget()
        holderWidget.setStyleSheet(f"background:{settings.BACKGROUND_WIDGET};");
        holderWidget.setLayout(self.gridLayout)

        holderLayout = QHBoxLayout()
        holderLayout.addWidget(holderWidget)

        self.setLayout(holderLayout)

    # I don't know, close enough :-
    def onResize(self, event) -> None:
        if event.size():
            self.dropLabel.setFixedWidth( self.recreatedImagePlot.width() - 50)
            self.dropLabel.setFixedHeight( self.recreatedImagePlot.height() - 20)
            self.dropLabel.onResize(self.recreatedImagePlot.width() - 50, self.recreatedImagePlot.height() - 20)

    def createImageLabel(self) -> QLabel:
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-weight: bold")
        return label

    def setRecreatedImage(
        self,
        ndarray : np.ndarray,
        title: str):
        self.setImage(ndarray, title)

    def selectedFileChanged(self, filePath: str) -> None:
        if filePath:
            self.fileDroppedSignal.emit(filePath)

            self.gridLayout.removeWidget(self.fftImage)
            self.fftImage.hide()
            self.gridLayout.addWidget(self.dropLabel, 1,0)

            self.dropLabel.changePicture(filePath)
            self.dropLabel.show()

    def selectedFFTChanged(self, filePath: str) -> None:
        if filePath:
            self.fftFileSelectedSignal.emit(filePath)

    def setFFTImage(self,
        ndarray : np.ndarray,
        ) -> None:

        self.fftImage.changeTitle("")
        self.fftImage.displayDataAsImage(ndarray, "viridis")
        self.fftImage.updateDrawing()
        self.gridLayout.removeWidget(self.dropLabel)
        self.gridLayout.addWidget(self.fftImage, 1,0)

        self.fftImage.show()
        self.dropLabel.hide()

    def setImage(
        self,
        ndarray : np.ndarray,
        title: str
        ) -> None:
        self.plotImage.changeTitle(title)
        self.plotImage.displayDataAsImage(ndarray, "viridis")
        self.plotImage.updateDrawing()

    def saveFile(self, filePath: str) -> None:
        if filePath:
            self.saveFileSignal.emit(filePath)

