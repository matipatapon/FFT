from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFormLayout, QSlider, QWidget, QLabel
from PySide6.QtCore import Qt, Signal
from calculations.constants import DEFAULT_THRESHOLD
import settings

class ThresholdSlider(QWidget):
    sliderValueChanged = Signal(float)
    def __init__(self):
        super().__init__()

        layout = QFormLayout()
        self.sliderValue: int = DEFAULT_THRESHOLD

        self.slider = QSlider(Qt.Orientation.Vertical, self)
        self.slider.setRange(1, 100)
        self.slider.setValue(self.sliderValue)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.slider.setFixedWidth(125)

        self.slider.setStyleSheet(self.getStyling())

        shouldEmitDuringDragging = False
        self.slider.setTracking(shouldEmitDuringDragging)

        self.slider.valueChanged.connect(self.onValueChange)
        self.slider.sliderMoved.connect(self.updateShownPercentage)

        self.valueInfo = QLabel()
        self.valueInfo.setFixedWidth(125)
        self.valueInfo.setStyleSheet("font-weight: bold;")
        self.valueInfo.setAlignment(Qt.AlignCenter)
        self.valueInfo.setText(f"Threshold: {self.sliderValue}%")

        layout.addRow(self.slider)
        layout.addRow(self.valueInfo)

        self.setLayout(layout)

    def updateShownPercentage(self, value: int) -> None:
        self.sliderValue = value
        self.valueInfo.setText(f"Threshold: {value}%")

    def onValueChange(self, value: int) -> None:
        self.updateShownPercentage(value)
        self.sliderValueChanged.emit((value)/100)

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



