from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel,QGridLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
import numpy as np
import settings

from gui.PlotWidget import PlotWidget
from gui.FileButton import FileButton

class DropWindow(QWidget):
    fileDroppedSignal = Signal(str)

    def __init__(self):
        super().__init__()

        self.plotWidgets: list[PlotWidget] = self.createPlotHolders()

        self.dropLabel = DropLabel()
        self.dropLabel.fileSelectedSignal.connect(self.selectedFileChanged)

        self.fileButton = FileButton();
        self.fileButton.fileSelectedSignal.connect(self.selectedFileChanged)

        self.gridLayout = self.createGrid()
        self.resizeEvent = self.onResize

        widgetHolder = QWidget()
        widgetHolder.setStyleSheet(f"background:{settings.BACKGROUND_WIDGET}; border-radius: 10px");
        widgetHolder.setLayout(self.gridLayout)

        holderLayout = QVBoxLayout()
        holderLayout.addWidget(widgetHolder)

        self.setLayout(holderLayout)

    def onResize(self, event) -> None:
        if event.size():
            newWidth: int = event.size().width()
            newHeight:int  = event.size().height()
            self.resizeGrid(newWidth, newHeight)

    def createGrid(self) -> QGridLayout:
        gridLayout = QGridLayout()
        gridLayout.setContentsMargins(10, 20, 10, 20)
        gridLayout.setSpacing(10)

        for i in range(5):
            gridLayout.setColumnStretch(i,3)

        gridLayout.setColumnStretch(5,1)

        gridLayout.addWidget(self.plotWidgets[0], 0, 0)
        gridLayout.addWidget(self.plotWidgets[1], 0, 1)
        gridLayout.addWidget(self.plotWidgets[2], 0, 2)
        gridLayout.addWidget(self.plotWidgets[3], 1, 0)
        gridLayout.addWidget(self.plotWidgets[4], 1, 1)
        gridLayout.addWidget(self.plotWidgets[5], 1, 2)

        gridLayout.addWidget(self.dropLabel, 0, 3, 2,2)
        gridLayout.addWidget(self.fileButton, 0, 5, 2 ,1)

        return gridLayout;

    def selectedFileChanged(self, filePath: str) -> None:
        if filePath:
            self.fileDroppedSignal.emit(filePath)
            self.dropLabel.changePicture(filePath)

    def createPlotHolders(self) -> list[PlotWidget]:
        plotHolders = []
        for  _ in range(6):
            plotHolders.append(PlotWidget())

        return plotHolders

    def resizeGrid(self, newWidth: int, newHeight: int) -> None:
        for plotWidget in self.plotWidgets:
            plotWidget.setMaximumSize(round(newWidth/2), round(newHeight/3))

        rectSize: int = round( newHeight/1.5 )
        self.dropLabel.setMaximumSize(rectSize, rectSize)

    def add_image_to_plot(
        self,
        ndarray : np.ndarray,
        position : int,
        title : str,
        color : bool
        ) -> None:

        if position >= len(self.plotWidgets):
            print("add_image ERROR:  Position out of bounds")
            return

        cmap = "viridis" if color else "gray"
        self.plotWidgets[position].changeTitle(title)
        self.plotWidgets[position].displayDataAsImage(ndarray, cmap)
        self.plotWidgets[position].updateDrawing()

class DropLabel(QLabel):
    fileSelectedSignal = Signal(str)
    def __init__(self):
        super().__init__()

        self.empty_label = None
        pixmap = QPixmap(settings.ASSETS_PATH + "/fileDropIcon.png")
        pixmap.setDevicePixelRatio(2)
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)
        self.resize(round( pixmap.height() / 8), round(pixmap.width() / 8))
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 4px dashed; border-radius: 4px")

    def dragEnterEvent(self, event) -> None:
        e = event
        if e.mimeData().hasFormat('text/plain') or e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, event) -> None:
        e = event
        img_path = e.mimeData().urls()[0].toLocalFile()
        if img_path:
            self.fileSelectedSignal.emit(img_path)

    def changePicture(self, imgPath: str) -> None:
        self.setPixmap(QPixmap(imgPath))
        self.setScaledContents(True)
        self.setStyleSheet("border: none")
