from PySide6.QtWidgets import QWidget, QVBoxLayout
from gui.DropWindow import DropWindow
from gui.ImageWindow import ImageWindow
import numpy as np

class PrimaryWindow(QWidget): 

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.topWindow = DropWindow()
        layout.addWidget(self.topWindow)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20);

        self.bottomWindow = ImageWindow()
        layout.addWidget(self.bottomWindow)

        layout.setStretch(0,1)
        layout.setStretch(1,1)

        self.setLayout(layout)

    def setPlots(
    self,
    ndarray : np.ndarray,
    position : int,
    title : str,
    color : bool):
        self.topWindow.add_image_to_plot(ndarray, position, title, color)

    def setRecreatedImage(
        self,
        ndarray : np.ndarray,
        title: str):
        self.bottomWindow.setImage(ndarray, title)

