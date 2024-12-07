from PySide6 import os
from PySide6.QtGui import QIcon, QPixmap, QCursor
from PySide6.QtWidgets import QSizePolicy, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PySide6.QtCore import Qt, Signal, QSize
import settings

class FileButton(QWidget):
    fileSelectedSignal = Signal(str)
    def __init__(self):
        super().__init__()

        button_label = QLabel(settings.DIRECTORY_ICON)
        button_label.setText("\n CHOOSE FILE \n")

        button_pixmap = QPixmap(settings.DIRECTORY_ICON)
        button_icon = QIcon(button_pixmap)
        button = QPushButton()
        button.setIcon(button_icon)
        button.setText("Choose file")
        icon_size = QSize(round(button_pixmap.width()/16), round(button_pixmap.height()/16))
        button.setIconSize(icon_size)
        button.clicked.connect(self.selectFile)
        button.setStyleSheet("""
            QPushButton {{
                background:{BG};
                padding: 10px;
                }}
            QPushButton:hover {{
                background: {hover};
            }}
            """.format(BG=settings.LIGHT_GRAY, hover=settings.NAVY_GRAY))
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.addWidget(button)

        self.setLayout(layout)


    def selectFile(self):
        self.filePath = QFileDialog.getOpenFileName(
            parent = QWidget(),
            caption = "Select file",
            dir = os.getcwd(),
            filter = "Image file (*.png *.jpg *.bmp)",
            selectedFilter = "Image file (*.png *.jpg *.bmp)"
        )
        if self.filePath:
            self.fileSelectedSignal.emit(self.filePath[0])
