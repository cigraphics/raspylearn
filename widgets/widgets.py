from PyQt4 import QtGui, QtCore

class Drawable(object):
    def __init__(self):
        self.qp = QtGui.QPainter()

    def draw(self):
        raise NotImplementedError

class Object2D(Drawable):
    def __init__(self):
        super(Object2D, self).__init__()

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_dim(self, width, height):
        self.width = width
        self.height = height

class Rect(Object2D):
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

class Elipse(Object2D):
    def __init__(self, x, y, width, height, color):
        super(Elipse, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.qp.setBrush(QtGui.QColor(*self.color))
        self.qp.drawEllipse(self.x, self.y, self.width, self.width)

class Image(Object2D):
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

def place_object_list(li, line_size, height = 0):
    count = len(li)
    size = line_size / count;
    depl = range(0, line_size, size)

    for i in range(count):
        li[i].set_dim(size, size)
        li[i].set_pos(depl[i], height)





