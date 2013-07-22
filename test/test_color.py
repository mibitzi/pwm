# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.xcb
import pwm.color


class TestColor(unittest.TestCase):
    def setUp(self):
        pwm.xcb.connect()
        pwm.xcb.setup_screens()

    def tearDown(self):
        pwm.xcb.disconnect()

    def test_get(self):
        self.assertEqual(pwm.color.get_pixel("#000000"),
                         pwm.xcb.screen.black_pixel)

        self.assertEqual(pwm.color.get_pixel("#ffffff"),
                         pwm.xcb.screen.white_pixel)
