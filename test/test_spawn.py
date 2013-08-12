# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import os
import time
import unittest
import subprocess

import pwm.spawn


class TestCommands(unittest.TestCase):
    def test_spawn(self):
        tmp_file = "/tmp/test_spawn"

        if os.path.isfile(tmp_file):
            os.unlink(tmp_file)

        pwm.spawn.spawn("touch %s" % tmp_file)
        subprocess.check_call("sync")

        self.assertTrue(os.path.isfile(tmp_file))

        os.unlink(tmp_file)
