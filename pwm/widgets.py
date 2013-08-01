# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function


def time(fmt="%Y-%m-%d %H:%M:%S", color=None):
    import time
    return (color, time.strftime(fmt))
