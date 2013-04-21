
from PyQt4 import QtGui, QtCore

images = {}

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

        # Compute the actual dimensions of the object according to the fill
        # percent and the width - height ratio
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

class Connection(Drawable):
    def __init__(self, grid, i1, j1, i2, j2, color = (100, 100, 100)):
        super(Connection, self).__init__()

        self.grid = grid
        self.cell = grid.generic_cell
        self.color = color

        # Compute the starting points of a connections. Those are in the midle
        # of the cells.
        self.x1 = i1 * self.cell.width + self.cell.width / 2
        self.y1 = j1 * self.cell.height + self.cell.height / 2

        self.x2 = i2 * self.cell.width + self.cell.width / 2
        self.y2 = j2 * self.cell.height + self.cell.height / 2

    def draw(self):
        self.qp.setBrush(QtGui.QColor(*self.color))
        self.qp.drawLine(self.x1, self.y1, self.x2, self.y2)


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

        # Use global images objects for less overhead.
        global images
        if images.get(self.image_path, None) == None:
            images[self.image_path] = QtGui.QImage(self.image_path)

        self.image = images[self.image_path]

    def draw(self):
        rect = QtCore.QRect(self.x, self.y, self.width, self.height)
        self.qp.drawImage(rect, self.image)

    def set_image(self, image_path):
        self.image_path = image_path
        self.image = QtGui.QImage(self.image_path)

    def highlight(self):
        self.image_path = "images/rasp_highlight.png"
        self.image = QtGui.QImage(self.image_path)

    def highlight_correct(self):
        self.image_path = "images/correct.png"
        self.image = QtGui.QImage(self.image_path)

    def highlight_incorrect(self):
        self.image_path = "images/incorrect.png"
        self.image = QtGui.QImage(self.image_path)
