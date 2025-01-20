from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QHBoxLayout, QListWidget, QPushButton, QSpacerItem, QVBoxLayout, QWidget,QSizePolicy
from PySide6.QtCore import Qt, Signal
import numpy as np
import settings

from gui.PlotWidget import PlotWidget

class StatsWindow(QWidget):
    getStatisticsSignal = Signal()

    def __init__(self):
        super().__init__()

        self.plotImage = PlotWidget()
        self.listWidget = self.createListWidget()
        self.button = self.createButton()

        listLayout = QVBoxLayout()
        listLayout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        listLayout.addWidget(self.listWidget)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.plotImage,3)
        topLayout.addLayout(listLayout,2)

        windowLayout = QVBoxLayout()
        windowLayout.addLayout(topLayout)
        windowLayout.addWidget(self.button,1)

        widgetHolder = QWidget()
        widgetHolder.setStyleSheet(f"background:{settings.BACKGROUND_WIDGET};")
        widgetHolder.setLayout(windowLayout)

        holderLayout = QVBoxLayout()
        holderLayout.addWidget(widgetHolder)

        self.setLayout(holderLayout)

    def createButton(self) -> QPushButton:
        button = QPushButton()
        button.setText("Calculate Statistics")
        button.clicked.connect(self.getStatisticsSignal.emit)
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
        return button

    def createListWidget(self) -> QListWidget:
        listWidget = QListWidget()
        listWidget.setStyleSheet("""
            QListWidget {
                background-color: #272c36;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
                background-color: #272c36;
            }
            QListWidget::item:selected {
                background-color: #121926;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #1b2028;
            }
        """)
        return listWidget

    def add_compressed_image(self, ndarray: np.ndarray) -> None:
        self.plotImage.displayDataAsImage(ndarray, "viridis")
        self.plotImage.updateDrawing()

    def setStatistics(self, statistics: list[str]):
        self.listWidget.clear()
        for stat in statistics:
            self.listWidget.addItem(stat)


