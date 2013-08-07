# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from collections import defaultdict

from pwm.config import config
import pwm.windows


class Action:
    def __init__(self, floating=False):
        self.floating = floating


rules = {"class": defaultdict(Action),
         "role": defaultdict(Action),
         "name": defaultdict(Action)}


def setup():
    """Create all rules as defined in the configuration."""

    for prop, val in config.floating:
        rules[prop][val.lower()].floating = True


def floating(wid):
    """Return true if this window matches any of the properties configured to
    float.
    """

    def _check(prop, value):
        if not value:
            return False

        value = value.lower()
        if value in rules[prop]:
            return rules[prop][value].floating
        else:
            return False

    return (_check("class", pwm.windows.get_wm_class(wid)) or
            _check("role", pwm.windows.get_wm_window_role(wid)) or
            _check("name", pwm.windows.get_name(wid)))
