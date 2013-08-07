# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest
from unittest.mock import patch

import pwm.match
import pwm.windows


class TestMatch(unittest.TestCase):
    def test_floating(self):
        pwm.match.rules["class"]["vlc"].floating = True

        with patch.object(pwm.windows, "get_wm_class",
                          return_value="Vlc"):
            self.assertTrue(pwm.match.floating(0))
