# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.workspaces
import pwm.layouts
import pwm.windows
import test.util as util


class TestLayouts(unittest.TestCase):
    def setUp(self):
        util.setup()

        self.workspace = pwm.workspaces.current()
        self.layout = pwm.layouts.Default(self.workspace)

        self.windows = [pwm.windows.Window(i)
                        for i in range(10)]

    def tearDown(self):
        util.tear_down()

    def test_default_add(self):
        self.layout.add(self.windows[0])

        self.assertEqual(self.layout.master, self.windows[0])
        self.assertEqual(self.layout.stacked, [])
        self.assertEqual(self.windows[0].x, 0)
        self.assertEqual(self.windows[0].y, 0)
        self.assertEqual(self.windows[0].width, self.workspace.width)
        self.assertEqual(self.windows[0].height, self.workspace.height)

        for i in range(1, 4):
            self.layout.add(self.windows[i])

            self.assertEqual(self.layout.stacked, self.windows[1:i+1])

            for s in self.layout.stacked:
                self.assertEqual(s.width, self.workspace.width / 2)
                self.assertEqual(s.height, self.workspace.height / i)

    def test_default_remove(self):
        for w in self.windows:
            self.layout.add(w)

        for i in range(len(self.windows)-1, 0, -1):
            self.layout.remove(self.windows[i])

            self.assertEqual(len(self.layout.stacked), i-1)

            for s in self.layout.stacked:
                self.assertEqual(s.width, self.workspace.width / 2)
                self.assertEqual(s.height, round(self.workspace.height/(i-1)))
