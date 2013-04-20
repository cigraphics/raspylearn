from PyQt4 import QtGui, QtCore

class Drawable(object):
    def __init__(self):
        self.qp = QtGui.QPainter()

    def draw(self):
        raise NotImplementedError

class Rect(Drawable):
    def __init__(self, x, y, width, height, color):
        super(Rect, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.qp.setBrush(QtGui.QColor(*self.color))
        self.qp.drawRect(self.x, self.y, self.width, self.height)

