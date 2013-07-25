# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import imp

import pwm.keybind
import pwm.xcb

config = None


class Key:
    """Class to store a command and the keys which it responds to."""
    def __init__(self, keys, command, *args, **kwargs):
        self.keys = keys
        self.command = command
        self.args = args
        self.kwargs = kwargs

    def call(self):
        return self.command(*self.args, **self.kwargs)


def load():
    global config
    config = imp.load_source("config", "config.py")


def setup_keys():
    for key in config.keys:
        mod, key = pwm.keybind.parse_keystring(key.keys)
        pwm.keybind.grab_key(pwm.xcb.screen.root, mod, key)
