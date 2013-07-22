# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.xcb


def get_pixel(color):
    if color.startswith("#"):
        if len(color) != 7:
            raise ValueError("Invalid color: %s" % color)

        def x8to16(i):
            return 0xffff * (i & 0xff) / 0xff

        r = x8to16(int(color[1] + color[2], 16))
        g = x8to16(int(color[3] + color[4], 16))
        b = x8to16(int(color[5] + color[6], 16))

        return pwm.xcb.core.AllocColor(pwm.xcb.screen.default_colormap,
                                       r, g, b).reply().pixel
    else:
        return pwm.xcb.core.AllocNamedColor(pwm.xcb.screen.default_colormap,
                                            len(color), color).reply().pixel
