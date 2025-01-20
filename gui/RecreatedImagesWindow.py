from PySide6.QtWidgets import QGridLayout, QWidget, QVBoxLayout
from gui.PlotWidget import PlotWidget
import numpy as np
import settings

class RecreatedImagesWindow(QWidget): 

    def __init__(self):
        super().__init__()

        self.plotWidgets: list[PlotWidget] = self.createPlotHolders()

        self.gridLayout = self.createGrid()

        widgetHolder = QWidget()
        widgetHolder.setStyleSheet(f"background:{settings.BACKGROUND_WIDGET};");
        widgetHolder.setLayout(self.gridLayout)

        holderLayout = QVBoxLayout()
        holderLayout.addWidget(widgetHolder)

        self.setLayout(holderLayout)

    def createPlotHolders(self) -> list[PlotWidget]:
        plotHolders = []
        for  _ in range(9):
            plotHolders.append(PlotWidget())

        return plotHolders

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
        self.plotWidgets[position].clear()
        self.plotWidgets[position].changeTitle(title)
        self.plotWidgets[position].displayDataAsImage(ndarray, cmap)
        self.plotWidgets[position].updateDrawing()


    def createGrid(self) -> QGridLayout:
        gridLayout = QGridLayout()
        gridLayout.setContentsMargins(10, 20, 10, 20)
        gridLayout.setSpacing(10)

        gridLayout.addWidget(self.plotWidgets[0], 0, 0)
        gridLayout.addWidget(self.plotWidgets[1], 0, 1)
        gridLayout.addWidget(self.plotWidgets[2], 0, 2)
        gridLayout.addWidget(self.plotWidgets[3], 1, 0)
        gridLayout.addWidget(self.plotWidgets[4], 1, 1)
        gridLayout.addWidget(self.plotWidgets[5], 1, 2)
        gridLayout.addWidget(self.plotWidgets[6], 2, 0)
        gridLayout.addWidget(self.plotWidgets[7], 2, 1)
        gridLayout.addWidget(self.plotWidgets[8], 2, 2)

        return gridLayout
