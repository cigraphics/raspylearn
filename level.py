from widgets import *
from threading import Thread
import time
import json

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

        # Can't inherit QWidget so hack this m0f0.
        self.signal_handler = self.SignalHandler()
        self.signal_handler.on_exception_raised.connect(editor.console_write,\
                            Qt.QueuedConnection)

        # Ugly callback so connect will work.
        def reload():
            self.load_skel()

        self.editor.reload_button.clicked.connect(reload)

        self.init()

    def load_skel(self):
        skel = open(self.skel, "r").read()
        self.editor.text_area.setPlainText(skel)

    def get_description(self):
        f = open(self.description, "r")
        res = f.read()
        # We should close more files.
        f.close()
        return res

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
    """Find the minimum of two numbers!"""

    method_name = "min"
    name = "MinNumber"
    skel = "skel/min.py"
    description = "description/min"

    def add_objects(self):
        self.values = {}

        grid = Grid(2, 3, 500, 500)

        # Generate the objects and use their dimensions as values.
        o1 = Image(grid, 0, 1, "images/rasp_logo.png", 30, 1.2)
        o2 = Image(grid, 1, 1, "images/rasp_logo.png", 70, 1.2)

        self.values[o1] = o1.fill;
        self.values[o2] = o2.fill;

        self.objects.append(o1)
        self.objects.append(o2)

        self.draw_area.add_object(o1)
        self.draw_area.add_object(o2)

    def check(self):
        x = self.method(self.values[self.objects[0]],
                        self.values[self.objects[1]])

        # We just happen to know the result.
        if x == 30:
            self.objects[0].highlight_correct()
        else:
            for o in self.objects:
                o.highlight_incorrect()

class MinNumberList(Level):
    """Find the minimum from a list of numbers!"""

    method_name = "min_list"
    name = "MinNumberList"
    skel = "skel/min_list.py"
    description = "description/min_list"

    def add_objects(self):
        grid = Grid(6, 5, 500, 500)

        self.vals = [4, 8, 6, 3, 5, 7]
        images = ["images/rasp_logo.png"] * len(self.vals)

        # Use predifined values to determine objects' sizes.
        for i in range(len(self.vals)):
            obj = Image(grid, i, 2, images[i], self.vals[i] * 10, 0.8)
            self.objects.append(obj)
            self.draw_area.add_object(obj)


    def check(self):
        x = self.method(self.vals)

        # Determine the min value of the list and check.
        if x == min(self.vals):
            self.objects[3].highlight_correct()
        else:
            for o in self.objects:
                o.highlight_incorrect()

class MaxNumberList(Level):
    """Find the maximum from a list of numbers!"""

    method_name = "max_list"
    name = "MaxNumberList"
    skel = "skel/max_list.py"
    description = "description/max_list"

    def add_objects(self):
        grid = Grid(6, 5, 500, 500)

        self.vals = [4, 8, 6, 3, 5, 7]
        images = ["images/rasp_logo.png"] * len(self.vals)

        # Use predifined values to determine objects' sizes.
        for i in range(len(self.vals)):
            obj = Image(grid, i, 2, images[i], self.vals[i] * 10, 0.8)
            self.objects.append(obj)
            self.draw_area.add_object(obj)


    def check(self):
        x = self.method(self.vals)

        # Determine the max value of the list and check.
        if x == max(self.vals):
            self.objects[1].highlight_correct()
        else:
            for o in self.objects:
                o.highlight_incorrect()

class BerrySearch(Level):
    """Help Barry the bear find the raspberry!"""

    method_name = "next_move"
    name = "BerrySearch"
    skel = "skel/dfs.py"
    description = "description/dfs"

    def add_objects(self):
        stuff = json.load(open("levels/dfs.json", "r"))

        matrix = stuff["matrix"]
        self.matrix = matrix

        # Set the grid according to the matrix size.
        grid = Grid(len(matrix), len(matrix[0]), 500, 500)

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if (matrix[i][j] == 0):
                    continue

                # Create objects images for each used square.
                obj = Image(grid, i, j, stuff[str(matrix[i][j])], 100, 0.8)
                self.objects.append(obj)
                self.draw_area.add_object(obj)
                if (i, j) == (8, 8):
                    self.rasp = obj

        self.bear = self.objects[11]

    def check(self):
        while True:
            x, y = self.method(self.matrix)
            self.bear.compute_position(x, y)

            if self.matrix[x][y] == 3:
                self.bear.highlight_incorrect()
                return

            # Barry found the raspberry.
            if (x, y) == (8, 8):
                self.bear.highlight_correct()
                self.rasp.highlight_correct()
                return

            self.draw_area.update()
            time.sleep(.5)

class BinaryTree(Level):
    """Traverse a binary tree!"""

    method_name = "tree_traversal"
    name = "BinaryTree"
    skel = "skel/bt.py"
    description = "description/bt"

    def add_objects(self):
        stuff = json.load(open("levels/binary_tree.json", "r"))

        mapping = {}
        connections = stuff["connections"]
        matrix = stuff["matrix"]
        self.matrix = matrix

        grid = Grid(len(matrix), len(matrix[0]), 500, 500)
        image = "images/rasp_logo.png"

        # Create objects for the nodes in the graph.
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if (matrix[i][j] == 0):
                    continue

                obj = Image(grid, i, j, image, 80, 1)
                self.objects.append(obj)

                mapping[(i, j)] = len(self.objects) - 1
        self.n = len(self.objects)

        # Create lines for the edges.
        for conn in connections:
            obj = Connection(grid, conn[0][1], conn[0][0],
                                   conn[1][1], conn[1][0])
            self.objects.append(obj)

        for obj in reversed(self.objects):
            self.draw_area.add_object(obj)

        self.edges = []
        for conn in connections:
            self.edges.append((mapping[tuple(conn[0])],
                               mapping[tuple(conn[1])]))


    def wrong_answer(self):
        for o in self.objects:
            o.highlight_incorrect()

    def check(self):

        traversal = self.method(0, self.edges)

        checked = {i: False for i in xrange(self.n)}
        for i in traversal:
            if i < 0:
                self.wrong_answer()
                return

            if i >= len(self.objects):
                self.wrong_answer()
                return

            checked[i] = True

            # Highlight objects in the transversal.
            self.objects[i].highlight()
            self.draw_area.update()
            time.sleep(.5)

        if False in checked.values():
            self.wrong_answer()


class Graph(Level):
    """ Graph Stongly Connected Components """

    method_name = "graph"
    name = "Graph"
    skel = "skel/graph.py"
    description = "description/graph"

    def add_objects(self):
        stuff = json.load(open("levels/graph.json", "r"))

        mapping = {}
        connections = stuff["connections"]
        matrix = stuff["matrix"]
        self.matrix = matrix

        grid = Grid(len(matrix), len(matrix[0]), 500, 500)
        image = "images/rasp_logo.png"

        # Create objects for the nodes in the graph.
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if (matrix[i][j] == 0):
                    continue

                obj = Image(grid, i, j, image, 120, 1)
                self.objects.append(obj)

                mapping[(i, j)] = len(self.objects) - 1
        self.n = len(self.objects)

        # Create lines for the edges.
        for conn in connections:
            obj = Connection(grid, conn[0][1], conn[0][0],
                                   conn[1][1], conn[1][0])
            self.objects.append(obj)

        for obj in reversed(self.objects):
            self.draw_area.add_object(obj)

        # Save edges as tuples of indexes.
        self.edges = []
        for conn in connections:
            self.edges.append((mapping[tuple(conn[0])],
                               mapping[tuple(conn[1])]))
            self.edges.append((mapping[tuple(conn[1])],
                               mapping[tuple(conn[0])]))


    def check(self):

        components = self.method(self.n, self.edges)
        count = 1

        for c in components:
            # Mark each component by its number.
            img = "images/img" + str(count) + ".png"
            for i in c:
                self.objects[i].set_image(img)

            time.sleep(1)
            self.draw_area.update()
            count += 1

classes = [ MinNumber, MinNumberList, MaxNumberList, BerrySearch,
            BinaryTree, Graph ]
