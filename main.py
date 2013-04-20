#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore

from widgets import *
from editor import Editor
import level
import inspect

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._setup()
        # A dictionary with all levels mapped like
        # { level_class_name : level_class }.
        self.levels_dict = {}

        self.draw_initial_menu()

        self.show()

    def _setup(self):
        self.setWindowTitle('RPI Learn you programming')

    def _get_all_classes(self, module):
        """Get all classes within a module."""
        return module.classes

    def draw_initial_menu(self):
        self.setMinimumSize(0, 0)
        self.setGeometry(0, 0, 300, 400)
        self.initial_menu_widget = QtGui.QWidget(self)

        self.setCentralWidget(self.initial_menu_widget)
        # Show the level selection, not a specific level.
        layout = QtGui.QVBoxLayout()

        # Draw initial choices for use to choose from.
        for level_class in self._get_all_classes(level):
            # Save the class instance by name.
            level_name = level_class.__name__
            level_desc = level_class.__doc__
            self.levels_dict[level_name] = level_class

            # Add button with name and description for each level.
            inside_layout = QtGui.QVBoxLayout()
            button = QtGui.QPushButton(level_name)
            button.clicked.connect(self.select_level)
            inside_layout.addWidget(button)
            label = QtGui.QLabel(level_desc)
            inside_layout.addWidget(label)
            layout.addLayout(inside_layout)

        self.initial_menu_widget.setLayout(layout)

    def select_level(self):
        # Switch to a selected level.
        sender_name = str(self.sender().text())
        # Get the level class which was selected by the user.
        level_class = self.levels_dict.get(sender_name)
        # Draw the selected level.
        self.draw_level(level_class)

    def draw_level(self, level_class):
        self.setGeometry(100, 100, 1024, 600)
        self.level_widget = QtGui.QWidget(self)

        self.setCentralWidget(self.level_widget)

        hbox = QtGui.QHBoxLayout()
        self.level_widget.setLayout(hbox)

        #draw area
        self.draw = DrawArea()

        #text area container
        self.editor = Editor()

        # Add a back button
        back_button = QtGui.QPushButton("< Back", self)
        back_button.clicked.connect(self.draw_initial_menu)

        container = QtGui.QWidget()
        container.setLayout(QtGui.QVBoxLayout())

        container.layout().addWidget(self.draw)
        container.layout().addWidget(back_button)

        hbox.addWidget(container)
        hbox.addWidget(self.editor)

        grid = Grid(6, 4, 500, 500)

        # Save the level class (e.g. MinNumber class level)
        # to use it to run the level selected by the user.
        self.level_class = level_class
        level = level_class(self.draw, self.editor)
        self.editor.on_execute.connect(self.start_level)

    def start_level(self, ns):
        level = self.level_class(self.draw, self.editor, False)
        level.set_method(ns[level.method_name])
        level.start()

class DrawArea(QtGui.QWidget):
    def __init__(self):
        super(DrawArea, self).__init__()
        self.setMinimumSize(500, 500)
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
