# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.xcb
import pwm.workspaces


class TestWindow(unittest.TestCase):
    def setUp(self):
        pwm.xcb.connect()
        pwm.xcb.setup_screens()

    def tearDown(self):
        pwm.xcb.disconnect()

    def test_geometry(self):
        workspace = pwm.workspaces.Workspace()

        self.assertEqual(workspace.x, 0)
        self.assertEqual(workspace.y, workspace.bar.height)
        self.assertEqual(workspace.width, pwm.xcb.screen.width_in_pixels)
        self.assertEqual(workspace.height, pwm.xcb.screen.height_in_pixels -
                         workspace.bar.height)
