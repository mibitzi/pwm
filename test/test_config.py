# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import os
import filecmp
import unittest

import pwm.config
import pwm.default_config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.path = "/tmp/pwmrc.py"
        self.config = pwm.config.Config()

    def tearDown(self):
        if os.path.isfile(self.path):
            os.remove(self.path)

    def test_ensure_config_exists_copy(self):
        self.config._ensure_config_exists(self.path)
        self.assertTrue(os.path.isfile(self.path))

    def test_ensure_config_exists_content(self):
        self.config._ensure_config_exists(self.path)
        self.assertTrue(filecmp.cmp(self.path, pwm.default_config.__file__))

    def test_ensure_config_exists_no_overwrite(self):
        with open(self.path, "w") as f:
            f.write("test")
        self.config._ensure_config_exists(self.path)

        with open(self.path, "r") as f:
            text = f.read()

        self.assertEqual(text, "test")
