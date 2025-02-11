from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
import settings

class InformationWindow(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout()
        showText = QTextEdit()
        showText.setReadOnly(True)
        showText.setHtml(self.load_html_file())

        mainLayout.addWidget(showText)
        self.setLayout(mainLayout)

    def load_html_file(self) -> str:
        file = QFile(settings.ASSETS_PATH + "/information.html")
        if not file.open(QFile.ReadOnly | QFile.Text):
            print("No such file")
            return ""

        text_stream = QTextStream(file)
        html_content = text_stream.readAll()

        file.close() 
        return html_content
