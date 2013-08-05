# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import os
import time
import unittest

import pwm.spawn


class TestCommands(unittest.TestCase):
    def test_spawn(self):
        tmp_file = "/tmp/test_spawn"

        if os.path.isfile(tmp_file):
            os.unlink(tmp_file)

        pwm.spawn.spawn("touch %s" % tmp_file)
        time.sleep(0.05)

        self.assertTrue(os.path.isfile(tmp_file))

        os.unlink(tmp_file)
