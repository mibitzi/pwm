# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from pwm.ffi.xcb import xcb

_atom_cache = {}


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


ROOT_MASK = (xcb.EVENT_MASK_STRUCTURE_NOTIFY |
             xcb.EVENT_MASK_SUBSTRUCTURE_NOTIFY |
             xcb.EVENT_MASK_SUBSTRUCTURE_REDIRECT |
             xcb.EVENT_MASK_ENTER_WINDOW |
             xcb.EVENT_MASK_LEAVE_WINDOW)


def setup_root_window():
    cookie = xcb.core.change_window_attributes_checked(
        xcb.screen.root,
        *xcb.mask([(xcb.CW_EVENT_MASK, ROOT_MASK)]))

    cookie.check()

    # We have to set the cursor now, otherwise it will not show up until the
    # first client is launched.
    set_root_cursor(Cursor.left_ptr)


def set_root_cursor(cursor):
    fid = xcb.core.generate_id()
    xcb.core.open_font(fid, len("cursor"), "cursor".encode("UTF-8"))

    cid = xcb.core.generate_id()
    xcb.core.create_glyph_cursor(cid, fid, fid, cursor, cursor+1,
                                 0, 0, 0, 65535, 65535, 65535)
    xcb.core.change_window_attributes(xcb.screen.root,
                                      *xcb.mask((xcb.CW_CURSOR, cid)))

    xcb.core.free_cursor(cid)
    xcb.core.close_font(fid)


def get_atom(atom_name, only_if_exists=False):
    """Query the X server for an ATOM identifier using a name. If we've already
    cached the identifier, then don't contact the X server.

    If the identifier is not cached, it is added to the cache.

    If 'only_if_exists' is false, then the atom is created if it does not exist
    already.
    """
    global _atom_cache

    if atom_name in _atom_cache:
        return _atom_cache[atom_name]

    atom = xcb.core.intern_atom_unchecked(only_if_exists, len(atom_name),
                                          atom_name.encode("UTF-8"))
    atom = atom.reply().atom
    _atom_cache[atom_name] = atom

    return atom
