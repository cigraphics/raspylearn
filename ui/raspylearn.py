#!/usr/bin/env python

import gtk
import pygame
import gobject
import os

width = 500
height = 400

class Window(gtk.Window):
    def __init__(self):
        super(Window, self).__init__()

        hbox = gtk.HBox()

        hbox.show()
        self.add(hbox)

        text_area = gtk.Entry()
        text_area.show()
        hbox.pack_end(text_area)

        drawing_area = gtk.DrawingArea()

        drawing_area.set_size_request(width, height)

        drawing_area.show()
        hbox.pack_end(drawing_area)

        drawing_area.connect("realize", self._realized)

    def _realized(self, widget, data=None):
        os.putenv('SDL_WINDOWID', str(widget.window.xid))

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill((0, 255, 255))
        gobject.timeout_add(200, self.draw)

    def draw(self):
        pygame.display.flip()
        return True

def main():
    window = Window()
    window.show()
    gtk.main()

if __name__ == "__main__":
    main()
