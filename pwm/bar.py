# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging
import threading
import cairo

from pwm.config import config
import pwm.xcb
import pwm.color as color
import pwm.events
import pwm.windows

primary = None
update_thread = None
stop_update = None
update_lock = None


class Bar:
    def __init__(self):
        self.width = pwm.xcb.screen.width_in_pixels
        self.height = calculate_height()

        self.workspaces_end = 0

        self.wid = self.create_window()
        self.pixmap = self.create_pixmap()
        self.gc = pwm.xcb.create_gc()
        (self.surface, self.ctx) = self.create_cairo_context()

    def destroy(self):
        pwm.windows.destroy(self.wid)
        pwm.xcb.core.FreePixmap(self.pixmap)
        pwm.xcb.core.FreeGC(self.gc)

    def create_window(self):
        return pwm.windows.create(0, 0, self.width, self.height)

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
        for depth in pwm.xcb.screen.allowed_depths:
            for visual in depth.visuals:
                if visual.visual_id == pwm.xcb.screen.root_visual:
                    return visual

    def create_cairo_context(self):
        surface = cairo.XCBSurface(
            pwm.xcb.conn,
            self.pixmap,
            self.find_root_visual(),
            self.width,
            self.height)

        ctx = cairo.Context(surface)

        ctx.select_font_face(config.bar.font.face)
        ctx.set_font_size(config.bar.font.size)

        return (surface, ctx)

    def draw_background(self):
        self.ctx.set_source_rgb(*color.get_rgb(config.bar.background))
        self.ctx.set_operator(cairo.OPERATOR_SOURCE)
        self.ctx.paint()

    def draw_open_workspaces(self):
        """Draw indicators for all open workspaces.

        Each open workspace is represented by a little box with
        a number in it.
        """

        # Figure out how big the boxes should be
        # Take the size of the text and add padding
        # Note that we have to align everything on 0.5 to avoid blurring
        extents = self.ctx.text_extents(
            "%d" % (len(pwm.workspaces.workspaces)-1))
        padding_left = 5
        box_width = extents[2] + 2*padding_left
        padding_top = 0.5
        box_height = self.height - 2*padding_top

        left = 0.5
        for widx, _ in pwm.workspaces.opened():
            fg = None
            bg = None
            border = None

            if widx == pwm.workspaces.current_workspace_index:
                fg = config.bar.active_workspace_foreground
                bg = config.bar.active_workspace_background
                border = config.bar.active_workspace_border
            else:
                fg = config.bar.inactive_workspace_foreground
                bg = config.bar.inactive_workspace_background
                border = config.bar.inactive_workspace_border

            # Draw the box
            self.ctx.set_source_rgb(*color.get_rgb(bg))
            self.ctx.rectangle(left, padding_top, box_width, box_height)
            self.ctx.fill()

            # Draw a border around the box
            self.ctx.set_source_rgb(*color.get_rgb(border))
            self.ctx.rectangle(left, padding_top,
                               box_width, box_height)
            self.ctx.set_line_width(1)
            self.ctx.stroke()

            # Draw the text
            text = "%d" % (widx+1)

            extents = self.ctx.text_extents(text)
            x_bearing, y_bearing, width, height, _, _ = extents

            center_x = left + box_width / 2
            center_y = padding_top + box_height/2
            self.ctx.move_to(center_x - x_bearing - width/2,
                             center_y - y_bearing - height/2)
            self.ctx.set_source_rgb(*color.get_rgb(fg))
            self.ctx.show_text(text)

            # Advance to the next position
            left += box_width + 2

        self.workspaces_end = left

    def draw_window_text(self):
        if not pwm.windows.focused:
            return

        text = pwm.windows.get_name(pwm.windows.focused)
        if text == "":
            return

        self.ctx.set_source_rgb(1, 1, 1)
        self.show_text(self.workspaces_end + 10, text)

    def draw_widgets(self):
        offset = 2
        for widget in reversed(config.bar.widgets):
            col, text = widget()

            if not col:
                col = config.bar.foreground

            extents = self.ctx.text_extents(text)
            x_bearing, y_bearing, width, height, _, _ = extents

            self.ctx.move_to(self.width - offset - width - x_bearing,
                             self.height/2 - y_bearing - height/2)
            self.ctx.set_source_rgb(*color.get_rgb(col))
            self.ctx.show_text(text)

            offset += width + 2

    def show_text(self, x, text):
        """Show text at the given x coordinate and vertically center it.

        Set font face and size as defined in the configuration.
        Return the used text extents.
        """

        extents = self.ctx.text_extents(text)
        _, y_bearing, _, height, _, _ = extents

        self.ctx.move_to(x, self.height/2 - (y_bearing + height/2))
        self.ctx.show_text(text)

        return extents

    def copy_pixmap(self):
        pwm.xcb.core.CopyArea(self.pixmap, self.wid, self.gc,
                              0, 0, 0, 0, self.width, self.height)

    def update(self):
        self.draw_background()
        self.draw_open_workspaces()
        self.draw_widgets()
        self.draw_window_text()
        self.copy_pixmap()

    def show(self):
        """Map the bar and update it."""
        pwm.xcb.core.MapWindow(self.wid)
        self.update()


def setup():
    global primary
    primary = Bar()
    primary.show()

    pwm.events.focus_changed.add(handle_focus_changed)
    pwm.events.window_property_changed.add(handle_window_property_changed)
    pwm.events.window_unmapped.add(handle_window_unmapped)
    pwm.events.workspace_switched.add(handle_workspace_switched)

    global stop_update
    global update_lock
    global update_thread
    stop_update = threading.Event()
    update_lock = threading.Lock()
    update_thread = threading.Thread(target=update_loop)
    update_thread.start()


def destroy():
    stop_update.set()

    update_thread.join(config.bar.interval*2)
    if update_thread.is_alive():
        logging.error("Bar updater did not stop, will be killed forcefully.")

    pwm.events.focus_changed.remove(handle_focus_changed)
    pwm.events.window_property_changed.remove(handle_window_property_changed)
    pwm.events.window_unmapped.remove(handle_window_unmapped)
    pwm.events.workspace_switched.remove(handle_workspace_switched)

    primary.destroy()


def update_loop():
    """Loop and update the bar until stop_update is set."""
    while True:
        if stop_update.wait(config.bar.interval):
            break
        update()


def update():
    """Update the bar."""
    if update_lock.acquire(False):
        try:
            primary.update()
            pwm.xcb.conn.flush()
        finally:
            update_lock.release()


def calculate_height():
    return config.bar.font.size + 8


def handle_focus_changed(wid):
    update()


def handle_window_property_changed(wid):
    if wid == pwm.windows.focused:
        update()


def handle_window_unmapped(wid):
    # Even if it was not the focused window, closing this window
    # might have caused a workspace to be closed
    update()


def handle_workspace_switched(idx):
    update()
