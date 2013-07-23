# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import xcb.xproto as xproto

from pwm.config import config
import pwm.xcb
import pwm.color
import pwm.workspaces


class Window:
    def __init__(self, wid):
        self.wid = wid
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.focused = False

        self.handle_focus(False)

        self.change_attributes(
            eventmask=(xproto.EventMask.EnterWindow |
                       xproto.EventMask.FocusChange |
                       xproto.EventMask.PropertyChange |
                       xproto.EventMask.StructureNotify))

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

        workspace = pwm.workspaces.current()

        mask, values = pwm.xcb.configure_mask(
            x=workspace.x + self.x,
            y=workspace.y + self.y,
            width=self.width - 2*config["border_width"],
            height=self.height - 2*config["border_width"],
            borderwidth=config["border_width"])
        pwm.xcb.core.ConfigureWindow(self.wid, mask, values)

    def handle_focus(self, focused):
        """Handles a change in focus.
        To focus a window use Workspace.focus
        """

        self.focused = focused

        border = None
        if self.focused:
            border = pwm.color.get_pixel(config["colors"]["focused"])
        else:
            border = pwm.color.get_pixel(config["colors"]["unfocused"])

        self.change_attributes(borderpixel=border)
