from highlight import PythonHighlighter
from PyQt4 import QtGui, QtCore, Qt
import sys

class Editor(QtGui.QWidget):
    on_execute = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(Editor, self).__init__()

        self.setLayout(QtGui.QVBoxLayout())

        label = QtGui.QLabel("Code:")

        #textedit and console output
        self.text_splitter = QtGui.QSplitter(self)
        self.text_splitter.setOrientation(2) # Qt.Vertical = 2.

        self.text_area = QtGui.QPlainTextEdit(self.text_splitter)
        self.console_output = QtGui.QPlainTextEdit(self.text_splitter)

        vertical_stretch = QtGui.QSizePolicy()
        vertical_stretch.setVerticalStretch(185)
        self.text_area.setSizePolicy(vertical_stretch)

        vertical_stretch_console = QtGui.QSizePolicy()
        vertical_stretch_console.setVerticalStretch(2)
        self.console_output.setSizePolicy(vertical_stretch_console)
        self.console_output.setMinimumHeight(60)

        PythonHighlighter(self.text_area.document())
        PythonHighlighter(self.console_output.document())

        self.text_splitter.addWidget(self.text_area)
        self.text_splitter.addWidget(self.console_output)

        # buttons
        run_button = QtGui.QPushButton("Run")
        self.reload_button = QtGui.QPushButton("Reload")

        self.layout().addWidget(label)
        self.layout().addWidget(self.text_splitter)
        self.layout().addWidget(run_button)
        self.layout().addWidget(self.reload_button)

        # connect run button
        run_button.clicked.connect(self.runPressed)

    def runPressed(self):
        print "run pressed."
        text = str(self.text_area.toPlainText())

        namespace = {}
        try:
            exec text in namespace
            self.on_execute.emit(namespace)
        except Exception as e:
            self.console_write(str(e))

    def console_write(self, text):
        self.console_output.setPlainText(text)
