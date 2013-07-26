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
    def __init__(self, keystr, command, *args, **kwargs):
        self.keystr = keystr
        self.command = command
        self.args = args
        self.kwargs = kwargs

        # Will be set in setup_keys
        self.mods = None
        self.keycode = None

    def call(self):
        return self.command(*self.args, **self.kwargs)


def setup_keys():
    for key in config.keys:
        key.mods, key.keycode = pwm.keybind.parse_keystring(key.keystr)
        pwm.keybind.grab_key(pwm.xcb.screen.root, key.mods, key.keycode)


class Config:
    def __init__(self):
        self.loaded = False
        self.data = None

    def load(self):
        self.loaded = True
        self.data = imp.load_source("config", "config.py")

    def __getattr__(self, name):
        if not self.loaded:
            self.load()

        return getattr(self.data, name)

config = Config()
