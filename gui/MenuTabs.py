from PySide6.QtWidgets import (
    QHBoxLayout,
    QTabWidget,
    QWidget,
)

class MenuTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setMovable(False)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.tabs)

        self.setLayout(hLayout)

    def addWidget(self, widget: QWidget, name: str):
        self.tabs.addTab(widget, name)

