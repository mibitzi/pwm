# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import unittest

from pwm.ffi.xcb import xcb
import pwm.color
import test.util as util


class TestColor(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    def test_get_pixl(self):
        self.assertEqual(pwm.color.get_pixel("#000000"),
                         xcb.screen.black_pixel)

        self.assertEqual(pwm.color.get_pixel("#ffffff"),
                         xcb.screen.white_pixel)

    def test_get_rgb(self):
        self.assertEqual(pwm.color.get_rgb("#000000"), (0, 0, 0))
        self.assertEqual(pwm.color.get_rgb("#ffffff"), (1, 1, 1))

        self.assertEqual(pwm.color.get_rgb("#ff0000"), (1, 0, 0))
        self.assertEqual(pwm.color.get_rgb("#00ff00"), (0, 1, 0))
        self.assertEqual(pwm.color.get_rgb("#0000ff"), (0, 0, 1))

        self.assertAlmostEqual(
            pwm.color.get_rgb("#1793D1"), (23/255, 147/255, 209/255))
