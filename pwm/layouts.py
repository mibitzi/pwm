# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging


class Default:
    def __init__(self, workspace):
        self.workspace = workspace
        self.focused = None
        self.master = None
        self.stacked = []
        self.master_width = self.workspace.width

    def add(self, window):
        if self.master is None:
            self.master = window
            self.resize(self.master, 0, 0)
        else:
            dx = 0
            if len(self.stacked) == 0:
                dx = self.workspace.width / 2

            self.stacked.append(window)

            window.width = 0
            window.height = 0

            self.resize(window, dx, self.workspace.height / len(self.stacked))

    def remove(self, window):
        if window == self.master:
            self.master = self.stacked.pop()
        elif window in self.stacked:
            self.stacked.remove(window)

    def resize(self, window, dx, dy):
        if window == self.master:
            self.master_width += dx
        elif window in self.stacked:
            self.master_width -= dx
            top = 0

            for w in self.stacked:
                height = w.height

                # Resize windows evenly
                if w != window:
                    height -= dy / (len(self.stacked) - 1)
                else:
                    height += dy

                x = self.master_width
                y = top
                width = self.workspace.width - self.master_width

                logging.debug(
                    ("configure stacked window: "
                     "x={}, y={}, width={}, height={}").
                    format(x, y, width, height))

                w.configure(x=x, y=y, width=width, height=height)

                top += height

        self.master.configure(x=0, y=0,
                              width=self.master_width,
                              height=self.workspace.height)
