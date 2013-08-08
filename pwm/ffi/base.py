# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import cffi

from pwm.ffi import headers


ffi = cffi.FFI()
ffi.cdef("""
void free(void *ptr);
""" + headers.xcb+headers.cairo)

lib = ffi.verify("""
    #include <stdlib.h>
    #include <xcb/xcb.h>
    #include <xcb/xproto.h>
    #include <xcb/xcb_aux.h>
    #include <xcb/xcb_event.h>
    #include <cairo/cairo.h>
    #include <cairo/cairo-xcb.h>
    """, libraries=["xcb", "xcb-util", "cairo"])
