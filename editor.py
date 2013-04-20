from highlight import PythonHighlighter
from PyQt4 import QtGui, QtCore
import sys

class Editor(QtGui.QWidget):
    on_execute = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(Editor, self).__init__()

        self.setLayout(QtGui.QVBoxLayout())

        label = QtGui.QLabel("Code:")
        self.text_area = QtGui.QPlainTextEdit()
        PythonHighlighter(self.text_area.document())

        button = QtGui.QPushButton("Run")

        self.layout().addWidget(label)
        self.layout().addWidget(self.text_area)
        self.layout().addWidget(button)


        # connect run button
        button.clicked.connect(self.runPressed)
        print button.clicked.__class__

    def runPressed(self):
        print "run pressed."
        text = str(self.text_area.toPlainText())

        namespace = {}
        exec text in namespace

        self.on_execute.emit(namespace)
        sys.stdout.flush()


