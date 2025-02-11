from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import settings


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.sc = PlotCanvas(self, width=5, height=19, dpi=100)

        self.sc.figure.tight_layout(pad=0)
        self.sc.axes.set_axis_off()

        self.sc.figure.set_facecolor(settings.BACKGROUND_WIDGET)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.sc)
        layout.addWidget(self.label)

        self.setLayout(layout)


    def changeTitle(self, title: str) -> None:
        self.label.setText(title)
        self.label.setMinimumSize(self.label.minimumSizeHint())

    def displayDataAsImage(
            self,
            ndarray : np.ndarray,
            cmap: str
            ):
        self.sc.axes.imshow(X = ndarray, cmap = cmap, aspect="equal")

    def updateDrawing(self) -> None:
        self.sc.draw()

    def clear(self) -> None:
        self.sc.axes.clear()
        self.sc.axes.set_axis_off()

class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super(PlotCanvas, self).__init__(fig)

