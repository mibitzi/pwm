# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import xcb.xproto as xproto

from pwm.config import config
import pwm.xcb
import pwm.color
import pwm.workspaces
import pwm.events

# wid: (window, workspace)
windows = {}

focused = None


class Window:
    def __init__(self, wid):
        self.wid = wid
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.visible = False

        self.change_attributes(
            eventmask=(xproto.EventMask.EnterWindow |
                       xproto.EventMask.FocusChange |
                       xproto.EventMask.PropertyChange |
                       xproto.EventMask.StructureNotify))

    def show(self):
        self.visible = True
        pwm.xcb.core.MapWindow(self.wid)

    def hide(self):
        self.visible = False
        pwm.xcb.core.UnmapWindow(self.wid)

    def change_attributes(self, **kwargs):
        mask, values = pwm.xcb.attribute_mask(**kwargs)
        pwm.xcb.core.ChangeWindowAttributes(self.wid, mask, values)

    def get_name(self):
        return pwm.xcb.get_property_string(self.wid, xproto.Atom.WM_NAME)

    def configure(self, **kwargs):
        """Arguments can be: x, y, width, height
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
            width=self.width - 2*config.window.border,
            height=self.height - 2*config.window.border,
            borderwidth=config.window.border)
        pwm.xcb.core.ConfigureWindow(self.wid, mask, values)

    def handle_focus(self, focused):
        """Set border color and input focus according to focus."""

        border = None
        if focused:
            border = pwm.color.get_pixel(config.window.focused)
        else:
            border = pwm.color.get_pixel(config.window.unfocused)

        self.change_attributes(borderpixel=border)

        if focused:
            pwm.xcb.core.SetInputFocus(xproto.InputFocus.PointerRoot,
                                       self.wid,
                                       xproto.Time.CurrentTime)


def handle_map_request(wid):
    win = Window(wid)
    ws = pwm.workspaces.current()

    ws.add_window(win)
    windows[wid] = (win, ws)


def handle_unmap_notification(win):
    _, ws = find(win.wid)
    ws.remove_window(win)
    del windows[win.wid]


def handle_focus(wid):
    global focused

    (win, ws) = windows.get(wid, (None, None))
    if not win or focused == win:
        return

    if focused:
        focused.handle_focus(False)

    focused = win
    focused.handle_focus(True)

    pwm.events.focus_changed(win)


def find(wid):
    return windows.get(wid, (None, None))
