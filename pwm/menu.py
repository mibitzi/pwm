# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import string
import re
import time
import logging

import pwm.windows
from pwm.config import config
from pwm.ffi.xcb import xcb
from pwm.ffi.cairo import cairo
import pwm.color
import pwm.keybind
import pwm.xdg
import pwm.spawn


active = False

_window = None
_height = 0
_width = 0
_pixmap = None
_gc = None
_surface = None
_ctx = None
_applications = None
_filtered = None
_selection = 0
_typed = ""


def setup():
    global _width
    _width = xcb.screen.width_in_pixels

    global _height
    _height = config.bar.font.size + 8

    global _window
    mask = [(xcb.CW_OVERRIDE_REDIRECT, 1),
            (xcb.CW_BACK_PIXEL, pwm.color.get_pixel(config.bar.background)),
            (xcb.CW_EVENT_MASK, xcb.EVENT_MASK_EXPOSURE)]
    _window = pwm.windows.create(0, 0, _width, _height, xcb.mask(mask))

    global _pixmap
    _pixmap = xcb.core.generate_id()
    xcb.core.create_pixmap(
        xcb.screen.root_depth,
        _pixmap,
        _window,
        _width,
        _height)

    global _gc
    _gc = xcb.core.generate_id()
    xcb.core.create_gc(_gc, xcb.screen.root,
                       *xcb.mask([(xcb.GC_FOREGROUND, xcb.screen.white_pixel),
                                  (xcb.GC_BACKGROUND, xcb.screen.black_pixel),
                                  (xcb.GC_GRAPHICS_EXPOSURES, 0)]))

    global _surface
    _surface = cairo.xcb_surface_create(
        xcb.conn,
        _pixmap,
        xcb.aux_find_visual_by_id(xcb.screen, xcb.screen.root_visual),
        _width,
        _height)

    global _ctx
    _ctx = cairo.create(_surface)

    _ctx.select_font_face(config.bar.font.face,
                          cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_NORMAL)
    _ctx.set_font_size(config.bar.font.size)


def destroy():
    xcb.core.destroy_window(_window)
    cairo.surface_destroy(_surface)
    _ctx.destroy()
    xcb.core.free_pixmap(_pixmap)
    xcb.core.free_gc(_gc)


def show():
    global active
    if active:
        return
    active = True

    global _typed
    _typed = ""

    global _applications
    _applications = pwm.xdg.applications()
    _filter_applist()

    xcb.core.map_window(_window)
    _draw()

    try:
        _grab_keyboard()
    except:
        logging.exception()
        _hide()


def _grab_keyboard():
    """Try to grab the keyboard."""

    # Try (repeatedly, if necessary) to grab the keyboard. We might not
    # get the keyboard at the first attempt because of the keybinding
    # still being active when started via a wm's keybinding.
    for _ in range(1000):
        reply = xcb.core.grab_keyboard(True, xcb.screen.root, xcb.CURRENT_TIME,
                                       xcb.GRAB_MODE_ASYNC,
                                       xcb.GRAB_MODE_ASYNC).reply()
        reply = xcb.ffi.cast("xcb_grab_keyboard_reply_t*", reply)
        if reply != xcb.ffi.NULL and reply.status == xcb.GRAB_STATUS_SUCCESS:
            return
        time.sleep(1.0/1000.0)

    raise Exception("Cannot grab keyboard")


def _hide():
    global active
    active = False

    xcb.core.unmap_window(_window)
    xcb.core.ungrab_keyboard(xcb.CURRENT_TIME)


def _filter_applist():
    global _selection
    _selection = 0

    global _filtered
    _filtered = []

    # Use a simple fuzzy search to match applications.
    #
    # 1. The pattern would be few characters.
    # 2. A match would mean that the characters in the pattern appear in the
    #    same order as in the matched string.
    # 3. A match found near the beginning of a string is scored more than a
    #    match found near the end.
    # 4. A match is scored more if the characters in the patterns are closer to
    #    each other, while the score is lower if they are more spread out.
    # 5. We are not assigning more weights to certain characters than the
    #    other.

    pattern = re.compile(
        ".*?".join(re.escape(char) for char in _typed.lower()))

    for idx, app in enumerate(_applications):
        match = pattern.search(app["name"].lower())
        if not match:
            continue

        score = 100 / ((1+match.start()) * (match.end() - match.start() + 1))

        # Insert:
        #   Inverted score for correct sorting
        #   Name to sort those with the same score (e.g. empty string typed)
        #   Index in case two applications have the same name
        #   Application information
        _filtered.append((-score, app["name"], idx, app))

    _filtered.sort()


def _draw():
    _ctx.set_source_rgb(*pwm.color.get_rgb(config.bar.background))
    _ctx.set_operator(cairo.OPERATOR_SOURCE)
    _ctx.paint()

    text = _typed+"|"

    font_ext = cairo.ffi.new("cairo_font_extents_t*")
    _ctx.font_extents(font_ext)
    pos_y = _height/2 - font_ext.descent + font_ext.height/2

    text_extents = cairo.ffi.new("cairo_text_extents_t*")
    _ctx.text_extents(text, text_extents)

    _ctx.move_to(0, pos_y)
    _ctx.set_source_rgb(*pwm.color.get_rgb(config.bar.foreground))
    _ctx.show_text(_typed+"|")

    left = max(font_ext.max_x_advance*20, text_extents.width+10)

    for idx, (_, _, _, app) in enumerate(_filtered):
        _ctx.text_extents(app["name"], text_extents)

        if idx == 0:
            # Make the first entry a bit nicer
            _ctx.set_source_rgb(*pwm.color.get_rgb(
                config.bar.active_workspace_background))
            _ctx.rectangle(left-5, 0, text_extents.width+10, _height)
            _ctx.fill()
            _ctx.set_source_rgb(*pwm.color.get_rgb(
                config.bar.active_workspace_foreground))
        else:
            _ctx.set_source_rgb(*pwm.color.get_rgb(
                config.bar.inactive_workspace_foreground))

        _ctx.move_to(left, pos_y)
        _ctx.show_text(app["name"])

        _ctx.text_extents(app["name"], text_extents)
        left += text_extents.width + 10

    xcb.core.copy_area(_pixmap, _window, _gc, 0, 0, 0, 0, _width, _height)


def handle_key_press_event(event):
    sym = pwm.keybind.get_keysym(event.detail, event.state)
    symstr = pwm.keybind.get_keysym_string(sym)

    if not symstr:
        return

    global _typed

    if symstr == "Escape":
        _hide()
        return

    elif symstr == "Return":
        if _filtered:
            # Strip out the placeholders some Exec values might have.
            pwm.spawn.spawn(
                _filtered[_selection][-1]["exec"].split(" ", 1)[0])
        _hide()
        return

    elif symstr == "BackSpace":
        _typed = _typed[:-1]

    else:
        sym = chr(sym)
        if sym not in string.printable:
            return

        _typed += sym

    _filter_applist()
    _draw()
