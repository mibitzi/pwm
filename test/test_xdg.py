# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import os
import glob
import unittest

import pwm.xdg


class TestXdg(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_desktop_file_dirs_home(self):
        self.assertIn(os.environ["HOME"] + "/.local/share/applications",
                      pwm.xdg.desktop_file_dirs())

    def test_desktop_file_dirs_sys(self):
        dirs = pwm.xdg.desktop_file_dirs()
        self.assertIn("/usr/local/share/applications", dirs)
        self.assertIn("/usr/share/applications", dirs)

    def test_find_desktop_files(self):
        found = pwm.xdg.find_desktop_files()
        for path in glob.glob("/usr/share/applications/*.desktop"):
            self.assertIn(path, found)

    def test_parse_desktop_file(self):
        content = "[Desktop Entry]\nName=Firefox\nExec=/usr/bin/firefox"
        self.assertEqual(pwm.xdg.parse_desktop_file(content),
                         {"name": "Firefox", "exec": "/usr/bin/firefox"})

    def test_applications(self):
        self.assertEqual(len(pwm.xdg.applications()),
                         len(pwm.xdg.find_desktop_files()))
