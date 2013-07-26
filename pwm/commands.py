# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.workspaces


def test(*args, **kwargs):
    return (args, kwargs)


def quit():
    exit()


def switch_workspace(index):
    pwm.workspaces.switch(index)


def kill():
    if pwm.windows.focused:
        pwm.windows.kill(pwm.windows.focused.wid)
