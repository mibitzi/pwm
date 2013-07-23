# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.xcb as xcb


class TestXcb(unittest.TestCase):

    def test_connect(self):
        xcb.connect()

        self.assertIsNotNone(xcb.conn)
        self.assertIsNotNone(xcb.core)
        self.assertEqual(xcb.core, xcb.conn.core)

        xcb.disconnect()

    def test_setup_screens(self):
        xcb.connect()

        xcb.setup_screens()

        self.assertIsNotNone(xcb.screen)
        self.assertEqual(xcb.screen, xcb.conn.get_setup().roots[0])

        xcb.disconnect()
