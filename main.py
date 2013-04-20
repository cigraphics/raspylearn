#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
from widgets import *
from editor import Editor
from level import MinNumber

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
        editor = Editor()

        hbox.addWidget(self.draw)
        hbox.addWidget(editor)

        self.draw.add_object(Rect(0, 0, 90, 90, (0, 200, 0)))
        self.draw.add_object(Circle(50, 50, 90, (0, 200, 0)))
        self.draw.add_object(Image(100, 100, 90, 110, "images/rasp_logo.png"))

        self.level = MinNumber(self.draw)
        #editor.on_execute.connect(self.start_level)

        self.setCentralWidget(self.central_widget)
        self.show()

    def start_level(self, ns):
        self.level.set_method(ns[self.level.method_name])
        self.level.start()


class DrawArea(QtGui.QWidget):
    def __init__(self):
        super(DrawArea, self).__init__()
        self.setMinimumSize(400, 600)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects = []

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
