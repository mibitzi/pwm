# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

from pwm.config import config
import pwm.xcb
import pwm.workspaces
import pwm.windows
import test.util as util


class TestWindow(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.wid = util.create_window()

    def tearDown(self):
        util.tear_down()

    def test_configure_geometry(self):
        pwm.windows.configure(self.wid, x=100, y=200, width=300, height=400)
        x, y, width, height = pwm.windows.get_geometry(self.wid)

        self.assertEqual(x, 100)
        self.assertEqual(y, 200 + pwm.workspaces.current().y)
        self.assertEqual(width, 300 - 2*config.window.border)
        self.assertEqual(height, 400 - 2*config.window.border)

    def test_show(self):
        pwm.windows.hide(self.wid)
        pwm.windows.show(self.wid)

        self.assertTrue(pwm.windows.is_mapped(self.wid))

    def test_hide(self):
        pwm.windows.hide(self.wid)
        self.assertFalse(pwm.windows.is_mapped(self.wid))

    def test_manage(self):
        win = util.create_window()
        self.assertIn(win, pwm.windows.managed)
        self.assertIn(win, pwm.workspaces.current().windows)
        self.assertEqual(win, pwm.windows.focused)

    def test_unmanage(self):
        wid = util.create_window()
        pwm.windows.unmanage(wid)
        self.assertNotIn(wid, pwm.windows.managed)
        self.assertNotIn(wid, pwm.workspaces.current().windows)
        self.assertNotEqual(wid, pwm.windows.focused)

    def test_handle_focus(self):
        wid2 = util.create_window()
        pwm.windows.handle_focus(wid2)
        self.assertEqual(pwm.windows.focused, wid2)

        pwm.windows.handle_focus(self.wid)
        self.assertEqual(pwm.windows.focused, self.wid)

        pwm.windows.handle_focus(None)
        self.assertEqual(pwm.windows.focused, None)
