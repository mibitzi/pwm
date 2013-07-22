# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import xcb
import xcb.xproto as xproto

conn = None

# Shortcut to conn.core
core = None

screen = None


def connect():
    """Connects to the X server"""

    global conn
    conn = xcb.connect(display=":1")

    global core
    core = conn.core


def disconnect():
    """Disconnects from the X server"""
    conn.disconnect()


def setup_screens():
    """Sets up all screens and root windows"""

    setup = conn.get_setup()

    global screen
    screen = setup.roots[0]

    root_event_mask = (xproto.EventMask.StructureNotify |
                       xproto.EventMask.SubstructureNotify |
                       xproto.EventMask.SubstructureRedirect |
                       xproto.EventMask.KeyPress)

    cookie = core.ChangeWindowAttributesChecked(
        screen.root,
        xproto.CW.EventMask, [root_event_mask])
    cookie.check()


# Stolen from Qtile
class MaskMap:
    """A general utility class that encapsulates the way the mask/value idiom
    works in xpyb. It understands a special attribute _maskvalue on
    objects, which will be used instead of the object value if present.
    This lets us passin a Font object, rather than Font.fid, for example.
    """
    def __init__(self, obj):
        self.mmap = []
        for i in dir(obj):
            if not i.startswith("_"):
                self.mmap.append((getattr(obj, i), i.lower()))
        self.mmap.sort()

    def __call__(self, **kwargs):
        """kwargs: keys should be in the mmap name set
        Returns a (mask, values) tuple.
        """
        mask = 0
        values = []
        for m, s in self.mmap:
            if s in kwargs:
                val = kwargs.get(s)
                if val is not None:
                    mask |= m
                    values.append(getattr(val, "_maskvalue", val))
                del kwargs[s]
        if kwargs:
            raise ValueError("Unknown mask names: %s" % kwargs.keys())
        return mask, values

configure_mask = MaskMap(xproto.ConfigWindow)
attribute_mask = MaskMap(xproto.CW)
gc_mask = MaskMap(xproto.GC)
