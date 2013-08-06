# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest

import test.util as util
from pwm.config import config
import pwm.workspaces
import pwm.state


class TestState(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    def reset(self):
        pwm.windows.handle_focus(None)
        pwm.windows.managed = {}
        pwm.workspaces.workspaces = []
        pwm.workspaces.current_workspace_index = 0

    def test_windows_managed(self):
        wid = util.create_window()
        pwm.state.store()
        self.reset()
        pwm.state.restore()

        self.assertIn(wid, pwm.windows.managed)

    def test_num_workspaces(self):
        pwm.state.store()
        self.reset()
        pwm.state.restore()
        self.assertEqual(len(pwm.workspaces.workspaces), config.workspaces)

    def test_windows_managed_workspace(self):
        wid = util.create_window()
        pwm.state.store()
        self.reset()
        pwm.state.restore()

        self.assertEqual(pwm.windows.managed[wid],
                         pwm.workspaces.workspaces[0])

    def test_workspace_windows(self):
        windows0 = pwm.workspaces.current().windows
        pwm.workspaces.switch(1)
        windows1 = pwm.workspaces.current().windows

        pwm.state.store()
        self.reset()
        pwm.state.restore()

        self.assertEqual(pwm.workspaces.workspaces[0].windows, windows0)
        self.assertEqual(pwm.workspaces.workspaces[1].windows, windows1)

    def test_focused(self):
        wid = util.create_window()

        pwm.state.store()
        self.reset()
        pwm.state.restore()
        self.assertEqual(pwm.windows.focused, wid)

    def test_current_workspace(self):
        pwm.workspaces.switch(1)

        pwm.state.store()
        self.reset()
        pwm.state.restore()

        self.assertEqual(pwm.workspaces.current(),
                         pwm.workspaces.workspaces[1])
