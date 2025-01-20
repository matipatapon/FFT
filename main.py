from PySide6.QtWidgets import QApplication
from gui.Gui import Gui
import sys
from Controller import Controller

def main():
    app = QApplication(sys.argv)
    gui = Gui()
    gui.show()

    controller = Controller(gui)

    gui.fileChangedSignal.connect(controller.changeFile)
    gui.fftFileChangedSignal.connect(controller.changeFFTFile)
    gui.saveFileSignal.connect(controller.saveFile)
    gui.thresholdChangedSignal.connect(controller.refreshFFT)
    gui.calculateStatisticsSignal.connect(controller.calculateCompressionStatistics)
    app.exec()

if __name__ == "__main__": 
    main()
