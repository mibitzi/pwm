# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import cffi

from pwm.ffi import headers


ffi = cffi.FFI()
ffi.cdef(headers.xcb+headers.cairo)

lib = ffi.verify("""
    #include <xcb/xcb.h>
    #include <xcb/xproto.h>
    #include <xcb/xcb_aux.h>
    #include <xcb/xcb_icccm.h>
    #include <cairo/cairo.h>
    #include <cairo/cairo-xcb.h>
    """, libraries=["xcb", "xcb-util", "xcb-icccm", "cairo"])
