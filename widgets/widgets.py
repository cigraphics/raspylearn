
from PyQt4 import QtGui, QtCore

class GridCell():
    def __init__(self, width, height, x = 0, y = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Grid():
    def __init__(self, n, m, width, height):
        self.n = n
        self.m = m
        self.image_width = width
        self.image_height = height

        self.generic_cell = GridCell(width / m, height / n)

class Drawable(object):
    def __init__(self):
        self.qp = QtGui.QPainter()

    def draw(self):
        raise NotImplementedError

class Object2D(Drawable):
    def __init__(self, grid, i, j, fill, ratio):
        super(Object2D, self).__init__()
        self.fill = fill
        self.ratio = ratio
        self.grid = grid
        self.cell = grid.generic_cell
        self.compute_position(i, j)

    def compute_position(self, i, j):
        self.cell.x = (self.cell.width * j)
        self.cell.y = (self.cell.height * i)

        self.width = (self.cell.width * self.fill * self.ratio) / 100
        self.height = (self.cell.height * self.fill) / 100

        self.x = self.cell.x + (self.cell.width - self.width) / 2
        self.y = self.cell.y + (self.cell.height - self.height) / 2

    def set_pos(self, i, j):
        self.compute_position(i, j)

    def highlight_correct(self):
        raise NotImplementedError

    def highlight_incorrect(self):
        raise NotImplementedError

class Rect(Object2D):
    def __init__(self, grid, i, j, color, fill, ratio = 1):
        super(Rect, self).__init__(grid, i, j, fill, ratio)
        self.color = color

    def draw(self):
        self.qp.setBrush(QtGui.QColor(*self.color))
        self.qp.drawRect(self.x, self.y, self.width, self.height)

    def highlight_correct(self):
        r, g, b = self.color
        self.color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))

    def highlight_incorrect(self):
        self.color = (255, 0, 0)

class Elipse(Object2D):
    def __init__(self, grid, i, j, color, fill, ratio = 1):
        super(Elipse, self).__init__(grid, i, j, fill, ratio)
        self.color = color

    def draw(self):
        self.qp.setBrush(QtGui.QColor(*self.color))
        self.qp.drawEllipse(self.x, self.y, self.width, self.height)

    def highlight_correct(self):
        r, g, b = self.color
        self.color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))

    def highlight_incorrect(self):
        self.color = (255, 0, 0)

class Image(Object2D):
    def __init__(self, grid, i, j, image_path, fill, ratio = 1):
        super(Image, self).__init__(grid, i, j, fill, ratio)
        self.image_path = image_path

    def draw(self):
        image = QtGui.QImage(self.image_path)
        rect = QtCore.QRect(self.x, self.y, self.width, self.height)
        self.qp.drawImage(rect, image)

    def highlight_correct(self):
        self.image_path = "images/correct.png"

    def highlight_incorrect(self):
        self.image_path = "images/incorrect.png"
