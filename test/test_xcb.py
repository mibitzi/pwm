# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function  # , unicode_literals

import unittest

import pwm.xcb


class TestXcb(unittest.TestCase):

    def setUp(self):
        pwm.xcb.connect()

    def tearDown(self):
        pwm.xcb.disconnect()

    def test_connect(self):
        self.assertIsNotNone(pwm.xcb.conn)
        self.assertIsNotNone(pwm.xcb.core)
        self.assertEqual(pwm.xcb.core, pwm.xcb.conn.core)

    def test_setup_screens(self):
        pwm.xcb.connect()

        pwm.xcb.setup_screens()

        self.assertIsNotNone(pwm.xcb.screen)
        self.assertEqual(pwm.xcb.screen, pwm.xcb.conn.get_setup().roots[0])

        pwm.xcb.disconnect()
