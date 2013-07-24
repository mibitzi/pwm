# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import xcb
import xcb.xproto as xproto
import cairo

from pwm.config import config
import pwm.xcb
import pwm.color as color


class Bar:
    def __init__(self, workspace):
        self.visible = False
        self.workspace = workspace

        self.width = self.workspace.width
        self.height = config["bar"]["height"]

        self.wid = self.create_window()
        self.pixmap = self.create_pixmap()
        self.gc = pwm.xcb.create_gc()
        (self.surface, self.ctx) = self.create_cairo_context()

        self.draw_pixmap()

    def create_window(self):
        wid = pwm.xcb.conn.generate_id()

        mask, values = pwm.xcb.attribute_mask(
            backpixel=pwm.xcb.screen.white_pixel,
            eventmask=xproto.EventMask.Exposure)

        pwm.xcb.core.CreateWindow(
            pwm.xcb.screen.root_depth,
            wid,
            pwm.xcb.screen.root,
            0, 0,  # x y
            self.width,
            self.height,
            0,  # border
            xproto.WindowClass.InputOutput,
            pwm.xcb.screen.root_visual,
            mask, values)

        return wid

    def create_pixmap(self):
        pixmap = pwm.xcb.conn.generate_id()

        pwm.xcb.core.CreatePixmap(
            pwm.xcb.screen.root_depth,
            pixmap,
            self.wid,
            self.width,
            self.height)

        return pixmap

    def find_root_visual(self):
        for i in pwm.xcb.screen.allowed_depths:
            for v in i.visuals:
                if v.visual_id == pwm.xcb.screen.root_visual:
                    return v

    def create_cairo_context(self):
        surface = cairo.XCBSurface(
            pwm.xcb.conn,
            self.pixmap,
            self.find_root_visual(),
            self.width,
            self.height)

        ctx = cairo.Context(surface)

        return (surface, ctx)

    def draw_background(self):
        self.ctx.set_source_rgb(*color.get_rgb(config["bar"]["background"]))
        self.ctx.set_operator(cairo.OPERATOR_SOURCE)
        self.ctx.paint()

    def draw_window_text(self):
        if not self.workspace.focused:
            return

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.select_font_face(config["bar"]["font"]["face"])
        self.ctx.set_font_size(config["bar"]["font"]["size"])

        text = self.workspace.focused.get_name()

        _, y_bearing, _, height, _, _ = self.ctx.text_extents(text)

        self.ctx.move_to(10, self.height/2 - (y_bearing + height/2))
        self.ctx.show_text(text)

    def copy_pixmap(self):
        pwm.xcb.core.CopyArea(self.pixmap, self.wid, self.gc,
                              0, 0, 0, 0, self.width, self.height)

    def draw_pixmap(self):
        self.draw_background()
        self.draw_window_text()

    def update(self):
        self.draw_pixmap()
        self.copy_pixmap()

    def show(self):
        """Renders the bar to its workspace"""
        self.visible = True

        pwm.xcb.core.MapWindow(self.wid)
        self.copy_pixmap()

    def hide(self):
        """Hides the bar from its workspace"""
        self.visible = False
        pwm.xcb.core.UnmapWindow(self.wid)
