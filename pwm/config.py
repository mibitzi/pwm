# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import yaml

config = {}


def load():
    contents = ""
    with open("config.yaml") as f:
        contents = f.read()

    global config
    config = yaml.safe_load(contents)

load()
