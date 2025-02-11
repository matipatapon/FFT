from PySide6.QtWidgets import (
    QHBoxLayout,
    QTabWidget,
    QWidget,
)

class MenuTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()

        self.tabs.setStyleSheet("""
            QWidget { 
                background-color: #272c36; 
                border: none;
            }
            QTabWidget {
                background-color: #272c36;
                color: white;
            }

            QTabBar::tab {
                background-color: #272c36;
                color: white;
                padding: 10px;
            }

            QTabBar::tab:selected {
                background-color: #3a3f50;
                color: white;
            }

            QTabBar::tab:hover {
                background-color: #3a3f50;
            }
        """)

        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setMovable(False)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.tabs)

        self.setLayout(hLayout)

    def addWidget(self, widget: QWidget, name: str) -> None:
        self.tabs.addTab(widget, name)

