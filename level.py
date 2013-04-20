from widgets import *
from threading import Thread
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Level(Thread):
    class SignalHandler(QtGui.QWidget):
        on_exception_raised = QtCore.pyqtSignal(str)

    def __init__(self, draw_area, editor, load_skel=True):
        super(Level, self).__init__()
        self.draw_area = draw_area
        self.editor = editor
        if load_skel:
            self.load_skel()

        # can't inherit QWidget so hack this m0f0
        self.signal_handler = self.SignalHandler()
        self.signal_handler.on_exception_raised.connect(editor.console_write,\
                            Qt.QueuedConnection)

        #Ugly callback so connect will work
        def reload():
            self.load_skel()

        self.editor.reload_button.clicked.connect(reload)

        self.init()

    def load_skel(self):
        skel = open(self.skel, "r").read()
        self.editor.text_area.setPlainText(skel)

    def init(self):
        self.draw_area.clear()
        self.objects = []
        self.add_objects()

    def set_method(self, method):
        self.method = method

    def add_objects(self):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def run(self):
        self.draw_area.update()
        try:
            self.check()
        except Exception as e:
            self.signal_handler.on_exception_raised.emit(str(e))

        self.draw_area.update()
        time.sleep(1)
        self.init()
        self.draw_area.update()

class MinNumber(Level):
    """Find the minimum of two numbers."""

    method_name = "min"
    name = "MinNumber"
    skel = "skel/min.py"

    def add_objects(self):
        self.values = {}

        grid = Grid(2, 1, 400, 600)

        o1 = Image(grid, 0, 0, "images/rasp_logo.png", 30, 0.8)
        o2 = Image(grid, 1, 0, "images/rasp_logo.png", 70, 0.8)

        self.values[o1] = o1.fill;
        self.values[o2] = o2.fill;

        self.objects.append(o1)
        self.objects.append(o2)

        self.draw_area.add_object(o1)
        self.draw_area.add_object(o2)

    def check(self):
        x = self.method(self.values[self.objects[0]], self.values[self.objects[1]])

        if x == 30:
            self.objects[0].highlight_correct()
        else:
            for o in self.objects:
                o.highlight_incorrect()

class MinNumberList(Level):
    """Find the minimum from a list of numbers."""

    method_name = "min_list"
    name = "MinNumberList"
    skel = "skel/min_list.py"

    def add_objects(self):
        grid = Grid(6, 1, 400, 600)

        self.vals = [4, 8, 6, 3, 5, 7]
        images = ["images/rasp_logo.png"] * len(self.vals)

        for i in range(len(self.vals)):
            obj = Image(grid, i, 0, images[i], self.vals[i] * 10, 0.3)
            self.objects.append(obj)
            self.draw_area.add_object(obj)


    def check(self):
        x = self.method(self.vals)

        if x == min(self.vals):
            self.objects[3].highlight_correct()
        else:
            for o in self.objects:
                o.highlight_incorrect()

classes = [ MinNumber, MinNumberList ]
