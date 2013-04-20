from highlight import PythonHighlighter
from PyQt4 import QtGui, QtCore

class Editor(QtGui.QWidget):
    def __init__(self):
        super(Editor, self).__init__()

        self.setLayout(QtGui.QVBoxLayout())

        button = QtGui.QPushButton("Run")
        text_area = QtGui.QPlainTextEdit()
        PythonHighlighter(text_area.document())

        self.layout().addWidget(text_area)
        self.layout().addWidget(button)

        # connect run button
        button.clicked.connect(self.runPressed)

    def runPressed(self):
        print "run pressed."
