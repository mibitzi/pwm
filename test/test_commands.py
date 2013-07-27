# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import os
import time
import unittest

import pwm.commands
import test.util as util


class TestCommands(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    def test_switch_workspace(self):
        pwm.commands.switch_workspace(1)

        self.assertEqual(pwm.workspaces.current(),
                         pwm.workspaces.workspaces[1])

    def test_spawn(self):
        tmp_file = "/tmp/test_spawn"

        if os.path.isfile(tmp_file):
            os.unlink(tmp_file)

        pwm.commands.spawn("touch %s" % tmp_file)
        time.sleep(0.05)

        self.assertTrue(os.path.isfile(tmp_file))

        os.unlink(tmp_file)
