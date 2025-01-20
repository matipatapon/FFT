from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import QSize, Qt, Signal
from matplotlib.backends.qt_compat import QtCore
import settings

class DropLabel(QLabel):
    fileSelectedSignal = Signal(str)

    def __init__(self):
        super().__init__()
        self.imagePath = settings.ASSETS_PATH + "/fileDropIcon.png"
        self._pixmap = self.getScaledPixmap(self.imagePath)

        self.setPixmap(self._pixmap)
        self.setAlignment(Qt.AlignCenter)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 4px dashed; border-radius: 4px;")

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

    def onResize(self, width: int, height: int) -> None:
        if self._pixmap:
            size = QSize(width, height)
            scaled_pixmap = QPixmap(self.imagePath).scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self._pixmap = scaled_pixmap
            self.setPixmap(scaled_pixmap)

    def changePicture(self, imgPath: str) -> None:
        self.imagePath = imgPath
        self._pixmap = self.getScaledPixmap(self.imagePath)
        self.setPixmap(self._pixmap)
        self.setStyleSheet("border: none")

    def getScaledPixmap(self, imgPath: str) -> QPixmap:
        pixmap = QPixmap(imgPath)
        size = self.calculatePixmapSize(pixmap, self.width())
        scaled_pixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return QPixmap(scaled_pixmap)

    def calculatePixmapSize(self, pixmap: QPixmap, desired_width) -> QSize:
        original_width = pixmap.width()
        original_height = pixmap.height()
        aspect_ratio = original_height / original_width
        new_height = int(desired_width * aspect_ratio)
        size=QSize(desired_width, new_height)
        return size
