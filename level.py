from widgets import *
from threading import Thread
import time

class Level(Thread):
    def __init__(self, draw_area):
        super(Level, self).__init__()
        self.draw_area = draw_area
        self.init()

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
    method_name = "min"
    name = "MinNumber"
    def add_objects(self):
        self.values = {}
        o1 = Rect(100, 50, 200, 200, (0, 200, 100))
        o2 = Rect(100, 300, 200, 200, (0, 200, 100))

        self.values[o1] = 3;
        self.values[o2] = 4;

        self.objects.append(o1)
        self.objects.append(o2)

        self.draw_area.add_object(o1)
        self.draw_area.add_object(o2)

    def check(self):
        x = self.method(self.values[self.objects[0]], self.values[self.objects[1]])
        if x == 3:
            self.objects[0].color = (0, 255, 0)
        else:
            color = (255, 0, 0)
            for o in self.objects:
                o.color = color

 
