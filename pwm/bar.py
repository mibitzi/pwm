# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import xcb.xproto as xproto
from pwm.config import config
import pwm.xcb as xcb
import pwm.color as color


class Bar:
    def __init__(self, workspace):
        self.visible = False
        self.workspace = workspace

        self.width = self.workspace.width
        self.height = config["bar"]["height"]

        self.wid = self.create_window()
        self.pixmap = self.create_pixmap()
        self.gc = xcb.create_gc()

        self.draw_pixmap()

    def create_window(self):
        wid = xcb.conn.generate_id()

        mask, values = xcb.attribute_mask(
            backpixel=xcb.screen.white_pixel,
            eventmask=xproto.EventMask.Exposure)

        xcb.core.CreateWindow(
            xcb.screen.root_depth,
            wid,
            xcb.screen.root,
            0, 0,  # x y
            self.width,
            self.height,
            0,  # border
            xproto.WindowClass.InputOutput,
            xcb.screen.root_visual,
            mask, values)

        return wid

    def create_pixmap(self):
        pixmap = xcb.conn.generate_id()

        xcb.core.CreatePixmap(
            xcb.screen.root_depth,
            pixmap,
            self.wid,
            self.width,
            self.height)

        return pixmap

    def draw_pixmap(self):
        xcb.change_gc(self.gc, foreground=color.get_pixel("#222222"))
        xcb.core.PolyFillRectangle(self.pixmap, self.gc, 1,
                                   (0, 0, self.width, self.height))

        xcb.change_gc(self.gc, foreground=color.get_pixel("#ffffff"))
        xcb.core.PolyPoint(xproto.CoordMode.Origin, self.pixmap,
                           self.gc,
                           1, (5, 5))

    def show(self):
        """Renders the bar to its workspace"""
        self.visible = True

        xcb.core.MapWindow(self.wid)
        xcb.core.CopyArea(self.pixmap, self.wid, self.gc,
                          0, 0, 0, 0, self.width, self.height)

    def hide(self):
        """Hides the bar from its workspace"""
        self.visible = False
        xcb.core.UnmapWindow(self.wid)
