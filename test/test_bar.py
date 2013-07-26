# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import xcb.xproto as xproto

import pwm.xcb
import pwm.workspaces
import pwm.bar
import test.util as util


class TestBar(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.bar = pwm.workspaces.bar

    def tearDown(self):
        util.tear_down()

    def test_show(self):
        self.bar.hide()
        self.bar.show()

        self.assertTrue(self.bar.visible)

        attr = pwm.xcb.core.GetWindowAttributes(self.bar.wid).reply()
        self.assertEqual(attr.map_state, xproto.MapState.Viewable)

    def test_hide(self):
        self.bar.hide()
        self.assertFalse(self.bar.visible)

        attr = pwm.xcb.core.GetWindowAttributes(self.bar.wid).reply()
        self.assertEqual(attr.map_state, xproto.MapState.Unmapped)
