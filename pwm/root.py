# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import logging

from pwm.ffi.xcb import xcb
import pwm.windows
import pwm.atom


class Cursor:
    fleur = 52
    left_ptr = 68
    sizing = 120
    bottom_left_corner = 12
    bottom_right_corner = 14
    top_left_corner = 134
    top_right_corner = 136
    double_arrow_horiz = 108
    double_arrow_vert = 116


EVENT_MASK = (xcb.EVENT_MASK_STRUCTURE_NOTIFY |
              xcb.EVENT_MASK_SUBSTRUCTURE_NOTIFY |
              xcb.EVENT_MASK_SUBSTRUCTURE_REDIRECT |
              xcb.EVENT_MASK_ENTER_WINDOW |
              xcb.EVENT_MASK_LEAVE_WINDOW)


def setup():
    """Setup the root window."""

    cookie = xcb.core.change_window_attributes_checked(
        xcb.screen.root,
        *xcb.mask([(xcb.CW_EVENT_MASK, EVENT_MASK)]))

    cookie.check()

    try:
        # We have to set the cursor now, otherwise it will not show up until
        # the first client is launched.
        set_cursor(Cursor.left_ptr)
    except:
        logging.exception("Root cursor error")

    try:
        _set_properties()
    except:
        logging.exception("Root properties error")


def set_cursor(cursor):
    fid = xcb.core.generate_id()
    xcb.core.open_font(fid, len("cursor"), "cursor".encode("UTF-8"))

    cid = xcb.core.generate_id()
    xcb.core.create_glyph_cursor(cid, fid, fid, cursor, cursor+1,
                                 0, 0, 0, 65535, 65535, 65535)
    xcb.core.change_window_attributes(xcb.screen.root,
                                      *xcb.mask((xcb.CW_CURSOR, cid)))

    xcb.core.free_cursor(cid)
    xcb.core.close_font(fid)


def _set_properties():
    # The root window must set certain properties, see:
    # See http://standards.freedesktop.org/wm-spec/latest/ar01s03.html

    # Let the clients know what window properties we support.
    supported = [
        "_NET_SUPPORTED",
        # "_NET_WM_STATE",
        # "_NET_WM_STATE_FULLSCREEN"
        "_NET_WM_NAME",
        #"_NET_WM_STRUT_PARTIAL",
        #"_NET_WM_ICON_NAME",
        #"_NET_WM_VISIBLE_ICON_NAME",
        #"_NET_WM_DESKTOP",
        "_NET_WM_WINDOW_TYPE",
        #"_NET_WM_WINDOW_TYPE_DESKTOP",
        #"_NET_WM_WINDOW_TYPE_DOCK",
        "_NET_WM_WINDOW_TYPE_TOOLBAR",
        #"_NET_WM_WINDOW_TYPE_MENU",
        "_NET_WM_WINDOW_TYPE_UTILITY",
        "_NET_WM_WINDOW_TYPE_SPLASH",
        "_NET_WM_WINDOW_TYPE_DIALOG",
        #"_NET_WM_WINDOW_TYPE_DROPDOWN_MENU",
        #"_NET_WM_WINDOW_TYPE_POPUP_MENU",
        #"_NET_WM_WINDOW_TYPE_TOOLTIP",
        #"_NET_WM_WINDOW_TYPE_NOTIFICATION",
        #"_NET_WM_WINDOW_TYPE_COMBO",
        #"_NET_WM_WINDOW_TYPE_DND",
        "_NET_WM_WINDOW_TYPE_NORMAL",
        #"_NET_WM_ICON",
        #"_NET_WM_PID",
        "_NET_WM_STATE",
        #"_NET_WM_STATE_STICKY",
        #"_NET_WM_STATE_SKIP_TASKBAR",
        "_NET_WM_STATE_FULLSCREEN",
        #"_NET_WM_STATE_MAXIMIZED_HORZ",
        #"_NET_WM_STATE_MAXIMIZED_VERT",
        #"_NET_WM_STATE_ABOVE",
        #"_NET_WM_STATE_BELOW",
        #"_NET_WM_STATE_MODAL",
        #"_NET_WM_STATE_HIDDEN",
        #"_NET_WM_STATE_DEMANDS_ATTENTION"
    ]

    atoms = [pwm.atom.get(name) for name in supported]
    pwm.windows.set_property(xcb.screen.root, "_NET_SUPPORTED", atoms)
