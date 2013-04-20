#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
from widgets import *
from highlight import PythonHighlighter

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Brushes')
        self.central_widget = QtGui.QWidget()

        hbox = QtGui.QHBoxLayout()
        self.central_widget.setLayout(hbox)

        #draw area
        self.draw = DrawArea()

        #text area container

        text_area_container = QtGui.QWidget()
        text_area_container.setLayout(QtGui.QVBoxLayout())

        button = QtGui.QPushButton("Run")
        text_area = QtGui.QPlainTextEdit()
        PythonHighlighter(text_area.document())


        text_area_container.layout().addWidget(text_area)
        text_area_container.layout().addWidget(button)

        hbox.addWidget(self.draw)
        hbox.addWidget(text_area_container)

        self.draw.add_object(Rect(0, 0, 90, 90, (0, 200, 0)))
        self.draw.add_object(Circle(50, 50, 90, (0, 200, 0)))
        self.draw.add_object(Image(100, 100, 90, 110, "images/rasp_logo.png"))

        self.setCentralWidget(self.central_widget)
        self.show()

class DrawArea(QtGui.QWidget):
    def __init__(self):
        super(DrawArea, self).__init__()
        self.setMinimumSize(400, 600)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def paintEvent(self, e):
        for o in self.objects:
            o.qp.begin(self)
            o.draw()
            o.qp.end()

def main():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
