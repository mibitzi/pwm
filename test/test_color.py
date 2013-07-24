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

    def test_get_pixl(self):
        self.assertEqual(pwm.color.get_pixel("#000000"),
                         pwm.xcb.screen.black_pixel)

        self.assertEqual(pwm.color.get_pixel("#ffffff"),
                         pwm.xcb.screen.white_pixel)

    def test_get_rgb(self):
        self.assertEqual(pwm.color.get_rgb("#000000"), (0, 0, 0))
        self.assertEqual(pwm.color.get_rgb("#ffffff"), (1, 1, 1))

        self.assertEqual(pwm.color.get_rgb("#ff0000"), (1, 0, 0))
        self.assertEqual(pwm.color.get_rgb("#00ff00"), (0, 1, 0))
        self.assertEqual(pwm.color.get_rgb("#0000ff"), (0, 0, 1))

        self.assertAlmostEqual(
            pwm.color.get_rgb("#1793D1"), (23/255, 147/255, 209/255))
