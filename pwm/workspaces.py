# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.xcb
import pwm.bar
import pwm.layouts

workspaces = []
current_workspace_index = 0


class Workspace:
    def __init__(self):
        self.windows = set([])

        self.bar = pwm.bar.Bar()

        self.x = 0
        self.y = self.bar.height

        self.width = pwm.xcb.screen.width_in_pixels
        self.height = pwm.xcb.screen.height_in_pixels - self.bar.height

        self.layout = pwm.layouts.Default(self)

    def add_window(self, window):
        self.windows.add(window)
        self.layout.add(window)
        window.show()

    def remove_window(self, window):
        self.windows.remove(window)
        self.layout.remove(window)

    def hide(self):
        for w in self.windows:
            w.hide()

    def show(self):
        for w in self.windows:
            w.show()


def add(workspace):
    workspaces.append(workspace)


def current():
    return workspaces[current_workspace_index]
