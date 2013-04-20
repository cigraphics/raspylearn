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

class Circle(Drawable):
    def __init__(self, x, y, r, color):
        super(Circle, self).__init__()
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self):
        self.qp.setBrush(QtGui.QColor(*self.color))
        self.qp.drawEllipse(self.x, self.y, self.r, self.r)

class Image(Drawable):
    def __init__(self, x, y, width, height, image_path):
        super(Image, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_path = image_path

    def draw(self):
        image = QtGui.QImage(self.image_path)
        rect = QtCore.QRect(self.x, self.y, self.width, self.height)
        self.qp.drawImage(rect, image)
        pass


