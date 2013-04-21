from highlight import PythonHighlighter
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

class LineNumberArea(QWidget):
    def __init__(self, code_editor):
        super(LineNumberArea, self).__init__(code_editor)
        self.code_editor = code_editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_paint(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent):
        super(CodeEditor, self).__init__(parent)
        self.line_number = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_width)
        self.updateRequest.connect(self.update_line_number)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_width(0)
        self.highlight_current_line()

    def line_number_paint(self, event):
        painter = QPainter(self.line_number)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = QString.number(block_num + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.line_number.width(),\
                    16, Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_num = block_num + 1

    def line_number_width(self):
        digits = 1
        mx = max(1, self.blockCount())
        while mx >= 10:
            mx = mx / 10
            digits = digits + 1
        space = 11 * digits
        return space

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.line_number.setGeometry(QRect(cr.left(), cr.top(),\
            self.line_number_width(), cr.height()))

    def update_line_number_width(self, size):
        self.setViewportMargins(self.line_number_width(), 0, 0, 0);

    def highlight_current_line(self):
        line_color = QColor(Qt.yellow).lighter(160)
        selection = QTextEdit.ExtraSelection()

        selection.format.setBackground(line_color)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        self.setExtraSelections([selection])

    def update_line_number(self, rect, size):
        if size:
            self.line_number.scroll(0, size)
        else:
            self.line_number.update(0, rect.y(), self.line_number.width(),\
                rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_width(0)

class Editor(QWidget):
    on_execute = pyqtSignal(dict)
    on_stop = pyqtSignal()

    def __init__(self):
        super(Editor, self).__init__()

        self.setLayout(QVBoxLayout())

        label = QLabel("Code:")

        # Textedit and console output.
        self.text_splitter = QSplitter(self)
        self.text_splitter.setOrientation(2) # Qt.Vertical = 2.

        self.text_area = CodeEditor(self.text_splitter)
        self.console_output = QPlainTextEdit(self.text_splitter)

        vertical_stretch = QSizePolicy()
        vertical_stretch.setVerticalStretch(185)
        self.text_area.setSizePolicy(vertical_stretch)

        vertical_stretch_console = QSizePolicy()
        vertical_stretch_console.setVerticalStretch(2)
        self.console_output.setSizePolicy(vertical_stretch_console)
        self.console_output.setMinimumHeight(60)
        self.console_output.setReadOnly(True)

        PythonHighlighter(self.text_area.document())
        PythonHighlighter(self.console_output.document())

        self.text_splitter.addWidget(self.text_area)
        self.text_splitter.addWidget(self.console_output)

        # Buttons.
        run_button = QPushButton("Run")
        run_button.setIcon(QIcon("images/play.png"))
        self.reload_button = QPushButton("Reload")
        self.reload_button.setIcon(QIcon("images/reload.png"))
        stop_button = QPushButton("Stop")
        stop_button.setIcon(QIcon("images/stop.png"))

        button_container = QWidget()
        button_container.setLayout(QHBoxLayout())
        button_container.setStyleSheet("QWidget { padding: 0px; }")

        button_container.layout().addWidget(run_button)
        button_container.layout().addWidget(stop_button)
        button_container.layout().addWidget(self.reload_button)

        self.layout().addWidget(label)
        self.layout().addWidget(self.text_splitter)
        self.layout().addWidget(button_container)

        # Connect run button.
        stop_button.clicked.connect(self.stop_pressed)
        run_button.clicked.connect(self.run_pressed)

        self.text_area.keyPressEvent = self.key_press

    def key_press(self, event):
        key = event.key()
        if key == Qt.Key_Tab:
            cursor = self.text_area.textCursor()
            cursor.insertText("    ")
        else:
            QPlainTextEdit.keyPressEvent(self.text_area, event)

    def stop_pressed(self):
        self.on_stop.emit()

    def run_pressed(self):
        self.console_write("Running simulation..")
        text = str(self.text_area.toPlainText())

        namespace = {}
        try:
            exec text in namespace
            self.on_execute.emit(namespace)
        except Exception as e:
            self.console_write(str(e))

    def console_write(self, text):
        self.console_output.setPlainText(text)
