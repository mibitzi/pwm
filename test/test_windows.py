# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest

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
        self.assertEqual(y, 200)
        self.assertEqual(width, 300)
        self.assertEqual(height, 400)

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

    def test_focus(self):
        wid2 = util.create_window()
        pwm.windows.focus(wid2)
        self.assertEqual(pwm.windows.focused, wid2)

        pwm.windows.focus(self.wid)
        self.assertEqual(pwm.windows.focused, self.wid)

        pwm.windows.focus(None)
        self.assertEqual(pwm.windows.focused, None)
