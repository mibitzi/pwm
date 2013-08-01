# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import cffi
import functools

from pwm.ffi.xcb import xcb
import pwm.ffi.headers as headers


class CairoError(Exception):
    pass


class Context:
    def __init__(self, ctx):
        self.ctx = ctx

    def __getattr__(self, name):
        return functools.partial(getattr(cairo.lib, "cairo_%s" % name),
                                 self.ctx)

    def encode(self, text):
        if type(text) == bytes:
            return text
        else:
            return text.encode("UTF-8")

    def select_font_face(self, face, slant, weight):
        return cairo.lib.cairo_select_font_face(self.ctx, self.encode(face),
                                                slant, weight)

    def text_extents(self, text, extents):
        return cairo.lib.cairo_text_extents(self.ctx, self.encode(text),
                                            extents)

    def show_text(self, text):
        return cairo.lib.cairo_show_text(self.ctx, self.encode(text))


class Cairo:
    """Wrapper class for the cairo functions.

    Cairo functions can be called on an instance of this class.
    """

    def __init__(self):
        self.ffi = cffi.FFI()
        self.ffi.include(xcb.ffi)
        self.ffi.cdef(headers.cairo)
        self.lib = self.ffi.verify("""
            #include <cairo/cairo.h>
            #include <cairo/cairo-xcb.h>
            """, libraries=["cairo"])

        self.cairo = None

    def __getattr__(self, name):
        try:
            return getattr(self.lib, "cairo_%s" % name)
        except:
            pass

        try:
            return getattr(self.lib, "CAIRO_%s" % name)
        except:
            pass

        return getattr(self.lib, name)

    def create(self, surface):
        return Context(self.lib.cairo_create(surface))


cairo = Cairo()
