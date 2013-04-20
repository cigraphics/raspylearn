#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
from widgets import *
from editor import Editor
from level import MinNumber

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._setup()

        # Main widgets for window.
        self.initial_menu_widget = QtGui.QWidget()
        self.level_widget = QtGui.QWidget()

        self.draw_initial_menu()

        self.show()

    def _setup(self):
        self.setWindowTitle('RPI Learn you programming')

    def get_levels(self):
        """Get all level names available for one to play."""
        return [('level1', 'desc1'), ('level2', 'desc2'), ('level3', 'desc2')]

    def draw_initial_menu(self):
        self.setCentralWidget(self.initial_menu_widget)

        layout = QtGui.QVBoxLayout()
        #layout.addStretch(1)

        # Draw initial choices for use to choose from.
        for level, desc in self.get_levels():
            inside_layout = QtGui.QVBoxLayout()

            button = QtGui.QPushButton(level)
            button.clicked.connect(self.selectLevel)
            inside_layout.addWidget(button)
            label = QtGui.QLabel(desc)
            inside_layout.addWidget(label)

            layout.addLayout(inside_layout)

        self.initial_menu_widget.setLayout(layout)

    def selectLevel(self):
        self.initial_menu_widget.close()
        self.draw_level()
        sender = self.sender()
        print(sender.text())

    def draw_level(self):
        self.setGeometry(300, 300, 800, 600)
        self.setCentralWidget(self.level_widget)

        hbox = QtGui.QHBoxLayout()
        self.level_widget.setLayout(hbox)

        #draw area
        self.draw = DrawArea()

        #text area container
        self.editor = Editor()

        hbox.addWidget(self.draw)
        hbox.addWidget(self.editor)

        grid = Grid(6, 4, 400, 600)

        self.draw.add_object(Elipse(grid, 0, 0, (0, 200, 0), 50))
        self.draw.add_object(Elipse(grid, 0, 1, (0, 200, 0), 10))
        self.draw.add_object(Elipse(grid, 1, 0, (0, 200, 0), 50))
        self.draw.add_object(Elipse(grid, 1, 1, (0, 200, 0), 10))

        self.draw.add_object(Image(grid, 0, 2, "images/rasp_logo.png", 70, 0.8))
        self.draw.add_object(Image(grid, 1, 2, "images/rasp_logo.png", 70, 0.8))
        self.draw.add_object(Image(grid, 0, 3, "images/rasp_logo.png", 70, 0.8))
        self.draw.add_object(Image(grid, 1, 3, "images/rasp_logo.png", 70, 0.8))

        self.draw.add_object(Image(grid, 2, 0, "images/tree.png", 100, 0.8))
        self.draw.add_object(Image(grid, 2, 1, "images/tree.png", 100, 0.8))
        self.draw.add_object(Image(grid, 3, 0, "images/tree.png", 100, 0.8))
        self.draw.add_object(Image(grid, 3, 1, "images/tree.png", 100, 0.8))

        self.draw.add_object(Rect(grid, 4, 0, (0, 200, 0), 50))
        self.draw.add_object(Rect(grid, 4, 1, (0, 200, 0), 50))

        level = MinNumber(self.draw, self.editor)
        self.editor.on_execute.connect(self.start_level)

    def start_level(self, ns):
        level = MinNumber(self.draw, self.editor, False)
        level.set_method(ns[level.method_name])
        level.start()

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
