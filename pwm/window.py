# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.xcb
import pwm.color

border_width = 1


class Window:
    def __init__(self, workspace, wid):
        self.workspace = workspace
        self.wid = wid
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.bordercolor = "#ff00ff"

        self.change_attributes(borderpixel=pwm.color.get_pixel("#ff00ff"))

    def show(self):
        pwm.xcb.core.MapWindow(self.wid)

    def hide(self):
        pwm.xcb.core.UnmapWindow(self.wid)

    def change_attributes(self, **kwargs):
        mask, values = pwm.xcb.attribute_mask(**kwargs)
        pwm.xcb.core.ChangeWindowAttributes(self.wid, mask, values)

    def configure(self, **kwargs):
        """ Arguments can be: x, y, width, height
        All changes to these variables should be done by calling this method.
        """

        self.x = int(kwargs.get("x", self.x))
        self.y = int(kwargs.get("y", self.y))
        self.width = int(kwargs.get("width", self.width))
        self.height = int(kwargs.get("height", self.height))

        mask, values = pwm.xcb.configure_mask(
            x=self.workspace.x + self.x,
            y=self.workspace.y + self.y,
            width=self.width - 2*border_width,
            height=self.height - 2*border_width,
            borderwidth=border_width)
        pwm.xcb.core.ConfigureWindow(self.wid, mask, values)
