from highlight import PythonHighlighter
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

class Editor(QWidget):
    on_execute = pyqtSignal(dict)

    def __init__(self):
        super(Editor, self).__init__()

        self.setLayout(QVBoxLayout())

        label = QLabel("Code:")

        #textedit and console output
        self.text_splitter = QSplitter(self)
        self.text_splitter.setOrientation(2) # Qt.Vertical = 2.

        self.text_area = QPlainTextEdit(self.text_splitter)
        self.console_output = QPlainTextEdit(self.text_splitter)

        vertical_stretch = QSizePolicy()
        vertical_stretch.setVerticalStretch(185)
        self.text_area.setSizePolicy(vertical_stretch)

        vertical_stretch_console = QSizePolicy()
        vertical_stretch_console.setVerticalStretch(2)
        self.console_output.setSizePolicy(vertical_stretch_console)
        self.console_output.setMinimumHeight(60)
        self.console_output.setReadOnly(True)

        PythonHighlighter(self.text_area.document())
        PythonHighlighter(self.console_output.document())

        self.text_splitter.addWidget(self.text_area)
        self.text_splitter.addWidget(self.console_output)

        # buttons
        run_button = QPushButton("Run")
        self.reload_button = QPushButton("Reload")

        self.layout().addWidget(label)
        self.layout().addWidget(self.text_splitter)
        self.layout().addWidget(run_button)
        self.layout().addWidget(self.reload_button)

        # connect run button
        run_button.clicked.connect(self.runPressed)
        self.text_area.keyPressEvent = self.key_press

    def key_press(self, event):
        key = event.key()
        if key == Qt.Key_Tab:
            cursor = self.text_area.textCursor()
            cursor.insertText("    ")
        else:
            QPlainTextEdit.keyPressEvent(self.text_area, event)

    def runPressed(self):
        self.console_write("")
        text = str(self.text_area.toPlainText())

        namespace = {}
        try:
            exec text in namespace
            self.on_execute.emit(namespace)
        except Exception as e:
            self.console_write(str(e))

    def console_write(self, text):
        self.console_output.setPlainText(text)
