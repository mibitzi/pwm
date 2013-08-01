# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import unittest

#import pwm.xcb
import test.util as util


class TestXcb(unittest.TestCase):

    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    #def test_connect(self):
    #    self.assertIsNotNone(pwm.xcb.conn)
    #    self.assertIsNotNone(pwm.xcb.core)
    #    self.assertEqual(pwm.xcb.core, pwm.xcb.conn.core)

    #def test_setup_screens(self):
    #    self.assertIsNotNone(pwm.xcb.screen)
    #    self.assertEqual(pwm.xcb.screen, pwm.xcb.conn.get_setup().roots[0])
