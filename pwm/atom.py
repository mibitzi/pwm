# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from pwm.ffi.xcb import xcb

_atom_cache = {}

_NET_WM_STATE_REMOVE = 0  # remove/unset property
_NET_WM_STATE_ADD = 1  # add/set property
_NET_WM_STATE_TOGGLE = 2  # toggle property


def get(atom_name, only_if_exists=False):
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


def get_name(atom):
    try:
        reply = xcb.core.get_atom_name(atom).reply()
    except:
        reply = None

    if not reply:
        return ""

    name = xcb.ffi.string(xcb.get_atom_name_name(reply), reply.name_len)
    name = name.decode("UTF-8")
    return name
