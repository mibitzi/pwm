# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals


class Default:
    def __init__(self, workspace):
        self.workspace = workspace
        self.focused = None
        self.master = None
        self.stacked = []

    def add(self, window):
        if self.master is None:
            self.master = window
        else:
            self.stacked.append(window)

        self.arrange()

    def remove(self, window):
        if window == self.master:
            if self.stacked:
                self.master = self.stacked.pop()
            else:
                self.master = None
        elif window in self.stacked:
            self.stacked.remove(window)

        self.arrange()

    def arrange(self):
        if self.master is None:
            return

        if not self.stacked:
            self.master.configure(x=0, y=0, width=self.workspace.width,
                                  height=self.workspace.height)
            return

        center = round(self.workspace.width / 2)
        self.master.configure(x=0, y=0, width=center,
                              height=self.workspace.height)

        height = self.workspace.height / len(self.stacked)
        top = 0
        for w in self.stacked:
            w.configure(x=center, y=round(top), width=center,
                        height=round(height))
            top += height
