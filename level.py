from widgets import *
from threading import Thread
import time

class Level(Thread):
    def __init__(self, draw_area, editor, load_skel=True):
        super(Level, self).__init__()
        self.draw_area = draw_area
        self.editor = editor
        if load_skel:
            self.load_skel()

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
        self.check()
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

        o1 = Image(grid, 0, 0, "images/rasp_logo.png", 30)
        o2 = Image(grid, 1, 0, "images/rasp_logo.png", 70)

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

classes = [ MinNumber ]
