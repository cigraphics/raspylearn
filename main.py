#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 300, 355, 280)
        self.setWindowTitle('Brushes')
        self.central_widget = QtGui.QWidget()

        hbox = QtGui.QHBoxLayout(self.central_widget)

        #draw area
        draw = DrawArea(self.central_widget)

        button = QtGui.QPushButton("OK")

        hbox.addWidget(draw)
        hbox.addWidget(button)

        self.setCentralWidget(self.central_widget)
        self.show()

class DrawArea(QtGui.QWidget):
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)

        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QtGui.QColor(200, 0, 0))
        qp.drawRect(30, 45, 90, 60)

        qp.end()

def main():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
