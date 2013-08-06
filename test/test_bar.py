# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest

import pwm.workspaces
import pwm.bar
import test.util as util


class TestBar(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    #def test_show(self):
    #    # show() should already have been called in setUp
    #    attr = pwm.xcb.core.GetWindowAttributes(self.bar.wid).reply()
    #    self.assertEqual(attr.map_state, xproto.MapState.Viewable)
