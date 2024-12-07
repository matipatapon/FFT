from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFormLayout, QSizePolicy, QSlider, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
import numpy as np
import settings

from gui.PlotWidget import PlotWidget


class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.show()

        layout = QHBoxLayout()

        self.imageLabel = PlotWidget()
        self.imageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.slider = ThresholdSlider()

        layout.addWidget(self.imageLabel)
        layout.addWidget(self.slider)

        holderWidget = QWidget()
        holderWidget.setStyleSheet(f"background:{settings.BACKGROUND_WIDGET}; border-radius: 10px");
        holderWidget.setLayout(layout)

        holderLayout = QHBoxLayout()
        holderLayout.addWidget(holderWidget)

        self.setLayout(holderLayout)

    def setImage(
        self,
        ndarray : np.ndarray,
        title: str
        ) -> None:
        self.imageLabel.changeTitle(title)
        self.imageLabel.displayDataAsImage(ndarray, "viridis")
        self.imageLabel.updateDrawing()


class ThresholdSlider(QWidget):
    sliderValueChanged = Signal(float)
    def __init__(self):
        super().__init__()

        layout = QFormLayout()
        self.sliderValue: int = 10

        self.slider = QSlider(Qt.Orientation.Vertical, self)
        self.slider.setRange(1, 100)
        self.slider.setValue(self.sliderValue)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider.setCursor(QCursor(Qt.PointingHandCursor))

        self.slider.setStyleSheet(self.getStyling())

        self.slider.valueChanged.connect(self.onValueChange)
        self.slider.sliderReleased.connect(self.onSliderRelease)

        self.valueInfo = QLabel()
        self.valueInfo.setFixedWidth(40)
        self.valueInfo.setStyleSheet("font-weight: bold;")
        self.valueInfo.setAlignment(Qt.AlignCenter)
        self.valueInfo.setText(f"{self.sliderValue}%")

        layout.addRow(self.slider)
        layout.addRow(self.valueInfo)

        self.setLayout(layout)

    def onValueChange(self, value: int) -> None:
        self.sliderValue = value
        self.valueInfo.setText(f"{value}%")

    def onSliderRelease(self) -> None:
        self.sliderValueChanged.emit((self.sliderValue)/100)

    def getStyling(self) -> str:
        return '''
            QSlider::groove:vertical{{
                width: 10px; 
                background-color: {grooveBg} ;
                border-radius: 4px;
            }}

            QSlider::handle:vertical{{ 
                background-color: {handleBG}; 
                height: 64px; 
                width: 20px; 
                margin-left: -5px; 
                margin-right: -5px; 
                border-radius: 10px; 
            }}
            QSlider::handle:vertical:hover {{
                border-radius: 10px;
                background: {hoverHandle};
            }}
            QSlider::add-page:vertical{{
                height: 16px;
                width: 16px;
                background: {pageBG};
            }}
            '''.format(grooveBg = settings.LIGHT_GRAY, 
                       handleBG = settings.SKY, 
                       hoverHandle = settings.LIGHT_SKY,
                       pageBG = settings.NAVY_GRAY)



