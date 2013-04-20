#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
from widgets import Rect

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 300, 355, 280)
        self.setWindowTitle('Brushes')
        self.central_widget = QtGui.QWidget()

        hbox = QtGui.QHBoxLayout()
        self.central_widget.setLayout(hbox)

        #draw area
        self.draw = DrawArea()
        button = QtGui.QPushButton("Run")
        text_area = QtGui.QPlainTextEdit()

        hbox.addWidget(self.draw)
        hbox.addWidget(button)
        hbox.addWidget(text_area)

        self.draw.add_object(Rect(0, 0, 90, 90, (0, 200, 0)))
        self.draw.add_object(Rect(0, 0, 90, 90, (0, 200, 0)))

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
