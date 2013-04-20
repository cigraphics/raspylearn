from highlight import PythonHighlighter
from PyQt4 import QtGui, QtCore
import sys

class Editor(QtGui.QWidget):
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

        self.on_execute = QtCore.SIGNAL("on_execute(1)")

        # connect run button
        button.clicked.connect(self.runPressed)

    def runPressed(self):
        print "run pressed."
        text = str(self.text_area.toPlainText())

        namespace = {}
        exec text in namespace

        self.emit(QtCore.SIGNAL("on_execute(1)"), namespace)
        sys.stdout.flush()


