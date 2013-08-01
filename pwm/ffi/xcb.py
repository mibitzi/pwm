# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import cffi
import functools
import re

import pwm.ffi.headers as headers


class XcbError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return "type %d code %d" % (self.error.response_type,
                                    self.error.error_code)


class Cookie:
    def __init__(self, name, value):
        self.name = name
        self.value = value

        self.name = re.sub("_unchecked$", "", self.name)

    def __getattr__(self, name):
        return getattr(self.value, name)

    def reply(self):
        error = xcb.ffi.new("xcb_generic_error_t**")

        reply = getattr(xcb.core, "%s_reply" % self.name)(self.value, error)
        if reply == xcb.ffi.NULL:
            raise XcbError(error)

        return reply

    def check(self):
        error = xcb.core.request_check(self.value)
        if error != xcb.ffi.NULL:
            raise XcbError(error)


class Xcb:
    """Wrapper class for the xcb functions.

    XCB functions can be called on an instance of this class.
    """

    def __init__(self):
        self.ffi = cffi.FFI()
        self.ffi.cdef(headers.xcb)
        self.lib = self.ffi.verify("""
            #include <xcb/xcb.h>
            #include <xcb/xproto.h>
            #include <xcb/xcb_aux.h>
            """, libraries=["xcb", "xcb-util"])

        self.conn = None
        self.setup = None
        self.call_core = False

    def __getattr__(self, name):
        def request(func, *args, **kwargs):
            retval = func(*args, **kwargs)

            try:
                ctype = self.ffi.getctype(self.ffi.typeof(retval))
                ctype = ctype.rstrip(" *")

                if ctype.endswith("cookie_t"):
                    return Cookie(name, retval)
            except:
                pass

            return retval

        if name == "core":
            self.call_core = True
            return self

        if self.call_core:
            self.call_core = False
            return functools.partial(
                request,
                functools.partial(getattr(self.lib, "xcb_%s" % name),
                                  self.conn))
        try:
            return functools.partial(
                request, getattr(self.lib, "xcb_%s" % name))
        except:
            pass

        try:
            return getattr(self.lib, "XCB_%s" % name)
        except:
            pass

        return functools.partial(request, getattr(self.lib, name))

    def connect(self, display=None):
        screen = self.ffi.new("int *")
        self.conn = self.lib.xcb_connect(display or self.ffi.NULL, screen)
        self.setup = self.core.get_setup()
        self.screen = self.core.aux_get_screen(screen[0])

    def mask(self, masks):
        # xcb requires mask-values to be sorted by their masks
        masks = sorted(masks, key=lambda m: m[0])
        values = self.ffi.new("uint32_t[]", [m[1] for m in masks])

        mask = 0
        for m in masks:
            mask |= m[0]

        return mask, values

xcb = Xcb()
