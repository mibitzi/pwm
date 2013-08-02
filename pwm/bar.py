# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import logging
import threading

from pwm.config import config
from pwm.ffi.xcb import xcb
from pwm.ffi.cairo import cairo
import pwm.color as color
import pwm.events
import pwm.windows

primary = None
update_thread = None
stop_update = None
update_lock = None


class Bar:
    def __init__(self):
        self.width = xcb.screen.width_in_pixels
        self.height = calculate_height()

        self.workspaces_end = 0
        self.systray_width = 0

        self.wid = self.create_window()
        self.pixmap = self.create_pixmap()
        self.gc = self.create_gc()
        (self.surface, self.ctx) = self.create_cairo_context()

    def destroy(self):
        pwm.windows.destroy(self.wid)
        cairo.surface_destroy(self.surface)
        self.ctx.destroy()
        xcb.core.free_pixmap(self.pixmap)
        xcb.core.free_gc(self.gc)

    def create_window(self):
        return pwm.windows.create(0, 0, self.width, self.height)

    def create_pixmap(self):
        pixmap = xcb.core.generate_id()

        xcb.core.create_pixmap(
            xcb.screen.root_depth,
            pixmap,
            self.wid,
            self.width,
            self.height)

        return pixmap

    def create_gc(self):
        gc = xcb.core.generate_id()

        xcb.core.create_gc(
            gc, xcb.screen.root,
            *xcb.mask([(xcb.GC_FOREGROUND, xcb.screen.white_pixel),
                       (xcb.GC_BACKGROUND, xcb.screen.black_pixel),
                       (xcb.GC_GRAPHICS_EXPOSURES, 0)]))

        return gc

    def create_cairo_context(self):
        surface = cairo.xcb_surface_create(
            xcb.conn,
            self.pixmap,
            xcb.aux_find_visual_by_id(xcb.screen, xcb.screen.root_visual),
            self.width,
            self.height)

        ctx = cairo.create(surface)

        ctx.select_font_face(config.bar.font.face,
                             cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(config.bar.font.size)

        return (surface, ctx)

    def text_extents(self, text):
        extents = cairo.ffi.new("cairo_text_extents_t*")
        self.ctx.text_extents(text, extents)
        return extents

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
        extents = self.text_extents(
            "%d" % (len(pwm.workspaces.workspaces)-1))
        padding_left = 5
        box_width = extents.width + 2*padding_left
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

            extents = self.text_extents(text)

            center_x = left + box_width / 2
            center_y = padding_top + box_height/2
            self.ctx.move_to(center_x - extents.x_bearing - extents.width/2,
                             center_y - extents.y_bearing - extents.height/2)
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
        offset = self.systray_width + 5
        for widget in reversed(config.bar.widgets):
            col, text = widget()

            if not col:
                col = config.bar.foreground

            extents = self.text_extents(text)

            self.ctx.move_to(
                self.width - offset - extents.width - extents.x_bearing,
                self.height/2 - extents.y_bearing - extents.height/2)
            self.ctx.set_source_rgb(*color.get_rgb(col))
            self.ctx.show_text(text)

            offset += extents.width + 2

    def show_text(self, x, text):
        """Show text at the given x coordinate and vertically center it.

        Set font face and size as defined in the configuration.
        Return the used text extents.
        """

        extents = self.text_extents(text)

        self.ctx.move_to(
            x,
            self.height/2 - (extents.y_bearing + extents.height/2))
        self.ctx.show_text(text)

        return extents

    def copy_pixmap(self):
        xcb.core.copy_area(self.pixmap, self.wid, self.gc,
                           0, 0, 0, 0, self.width, self.height)

    def update(self):
        self.draw_background()
        self.draw_open_workspaces()
        self.draw_widgets()
        self.draw_window_text()
        self.copy_pixmap()

    def update_systray(self, width):
        self.systray_width = width
        update()

    def show(self):
        """Map the bar and update it."""
        xcb.core.map_window(self.wid)
        update()


def setup():
    global stop_update
    global update_lock
    global update_thread
    stop_update = threading.Event()
    update_lock = threading.Lock()
    update_thread = threading.Thread(target=update_loop)

    global primary
    primary = Bar()
    primary.show()

    pwm.events.focus_changed.add(handle_focus_changed)
    pwm.events.window_property_changed.add(handle_window_property_changed)
    pwm.events.window_unmapped.add(handle_window_unmapped)
    pwm.events.workspace_switched.add(handle_workspace_switched)

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
            xcb.core.flush()
        except:
            logging.exception("Bar update error")
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
