# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from pwm.config import config
from pwm.ffi.xcb import xcb
from pwm.ffi.cairo import cairo
import pwm.color as color
import pwm.events
import pwm.windows
import pwm.widgets

primary = None


class Bar:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = xcb.screen.width_in_pixels
        self.height = calculate_height()

        self.workspaces_end = 0
        self.systray_width = 0

        self.wid = self.create_window()
        self.pixmap = self.create_pixmap()
        self.gc = self.create_gc()
        (self.surface, self.ctx) = self.create_cairo_context()
        self.extents = self.font_extents()
        self.center_y = (self.height/2 - self.extents.descent +
                         self.extents.height/2)

        self.handlers = pwm.events.HandlerList()
        self.handlers.add(pwm.events.focus_changed, self.handle_focus_changed)
        self.handlers.add(pwm.events.window_name_changed,
                          self.handle_window_name_changed)
        self.handlers.add(pwm.events.window_unmapped,
                          self.handle_window_unmapped)
        self.handlers.add(pwm.events.workspace_switched,
                          self.handle_workspace_switched)
        self.handlers.add(pwm.events.window_exposed,
                          self.handle_window_exposed)

    def destroy(self):
        self.handlers.destroy()
        pwm.windows.destroy(self.wid)
        cairo.surface_destroy(self.surface)
        self.ctx.destroy()
        xcb.core.free_pixmap(self.pixmap)
        xcb.core.free_gc(self.gc)

    def create_window(self):
        mask = [(xcb.CW_OVERRIDE_REDIRECT, 1),
                (xcb.CW_BACK_PIXEL, color.get_pixel(config.bar.background)),
                (xcb.CW_EVENT_MASK, xcb.EVENT_MASK_EXPOSURE)]

        return pwm.windows.create(self.x, self.y, self.width, self.height,
                                  xcb.mask(mask))

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

    def font_extents(self):
        extents = cairo.ffi.new("cairo_font_extents_t*")
        self.ctx.font_extents(extents)
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
        ws_chars = len("%d" % (len(pwm.workspaces.workspaces)-1))
        padding_left = 5
        box_width = self.extents.max_x_advance*ws_chars + 2*padding_left
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

            center_x = left + box_width / 2
            self.ctx.move_to(center_x - self.extents.max_x_advance*len(text)/2,
                             self.center_y)
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
        self.ctx.move_to(self.workspaces_end + 10, self.center_y)
        self.ctx.show_text(text)

    def draw_widgets(self):
        offset = self.systray_width + 5
        for widget in reversed(pwm.widgets.output):
            col, text = widget

            if not col:
                col = config.bar.foreground

            width = self.extents.max_x_advance*len(text)
            self.ctx.move_to(
                self.width - offset - width,
                self.center_y)
            self.ctx.set_source_rgb(*color.get_rgb(col))
            self.ctx.show_text(text)

            offset += width + 2

    def copy_pixmap(self):
        xcb.core.copy_area(self.pixmap, self.wid, self.gc,
                           0, 0, 0, 0, self.width, self.height)

    def update(self):
        """Update the bar."""
        self.draw_background()
        self.draw_open_workspaces()
        self.draw_widgets()
        self.draw_window_text()
        self.copy_pixmap()

    def update_systray(self, width):
        self.systray_width = width
        self.update()

    def show(self):
        """Map the bar and update it."""
        xcb.core.map_window(self.wid)
        self.update()

    def handle_focus_changed(self, wid):
        self.update()

    def handle_window_name_changed(self, wid):
        if wid == pwm.windows.focused:
            self.update()

    def handle_window_unmapped(self, wid):
        # Even if it was not the focused window, closing this window
        # might have caused a workspace to be closed
        self.update()

    def handle_workspace_switched(self, idx):
        self.update()

    def handle_window_exposed(self, wid):
        if wid == self.wid:
            self.copy_pixmap()


def setup():
    global primary
    primary = Bar()
    primary.show()


def destroy():
    primary.destroy()


def calculate_height():
    return config.bar.font.size + 8
