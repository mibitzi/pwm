# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from pwm.ffi.xcb import xcb


def get_pixel(color):
    if color.startswith("#"):
        if len(color) != 7:
            raise ValueError("Invalid color: %s" % color)

        def x8to16(i):
            return int(0xffff * (i & 0xff) / 0xff)

        r = x8to16(int(color[1] + color[2], 16))
        g = x8to16(int(color[3] + color[4], 16))
        b = x8to16(int(color[5] + color[6], 16))

        return xcb.core.alloc_color(xcb.screen.default_colormap,
                                    r, g, b).reply().pixel
    else:
        return xcb.core.alloc_named_color(xcb.screen.default_colormap,
                                          len(color), color).reply().pixel


def get_rgb(color):
    """Convert a hex color value to a rgb tuple with range 0-1."""
    value = color.lstrip('#')
    lv = len(value)
    step = int(lv/3)
    return tuple(int(value[i:i+step], 16)/255 for i in range(0, lv, step))
