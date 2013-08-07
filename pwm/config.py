# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import os
import errno
import functools
import logging
import importlib
from importlib.machinery import SourceFileLoader
import pkg_resources

import pwm.keybind
from pwm.ffi.xcb import xcb
import pwm.xdg

config = None
grabbed_keys = {}


class Config:
    def __init__(self):
        self.data = None
        self.path = pwm.xdg.config_home()+"/pwm/pwmrc.py"

    def load(self):
        try:
            self._ensure_config_exists(self.path)
            loader = SourceFileLoader("config", self.path)
            self.data = loader.load_module()
        except:
            logging.exception("Configuration error, falling back to default")
            self.data = importlib.import_module("pwm.default_config")

    def _ensure_config_exists(self, path):
        """Copy the default configuration to path if it not already exists."""
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

        if not os.path.isfile(path):
            default = pkg_resources.resource_string(__name__,
                                                    "default_config.py")

            # Note that we must pass "x" as mode.
            with open(path, "xb") as f:
                f.write(default)

    def __getattr__(self, name):
        return getattr(self.data, name)


def setup_keys():
    """Parse and grab all keys defined in the configuration."""

    for key in config.keys:
        keystr = key[0]
        mods, keycode = pwm.keybind.parse_keystring(keystr)

        if keycode:
            pwm.keybind.grab_key(xcb.screen.root, mods, keycode)

            grabbed_keys[(mods, keycode)] = key
        else:
            # This is not a critical error, we just can't respond to that key
            logging.error("Could not parse keybinding: {}".format(keystr))


def handle_key_press_event(event):
    """Search for a command to handle this KeyPressEvent and call it."""

    # Strip out all trivial modifiers such as capslock or numlock.
    # Then check if the key was grabbed
    mods, keycode = event.state, event.detail
    mods = pwm.keybind.strip_trivial(mods)

    key = grabbed_keys.get((mods, keycode))
    if key:
        try:
            key[1]()
        except:
            logging.exception("Command error")


def create_arguments(func):
    """A function decorator. When the function is called store the arguments
    and return a new function with those arguments already set.

    Used to pass functions with arguments in the config file.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return functools.partial(func, *args, **kwargs)
    return wrapper


config = Config()
