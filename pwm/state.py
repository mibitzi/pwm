# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import pickle

import pwm.workspaces
import pwm.windows


state_file = "/tmp/pwm.state"


def store():
    """Store the current state in the state file."""
    with open(state_file, "wb") as f:
        pickler = pickle.Pickler(f)
        pickler.dump(pwm.workspaces.workspaces)
        pickler.dump(pwm.workspaces.current_workspace_index)
        pickler.dump(pwm.windows.managed)
        pickler.dump(pwm.windows.ignore_unmaps)
        pickler.dump(pwm.windows.focused)


def restore():
    """Restore the current state from the state file."""
    with open(state_file, "rb") as f:
        unpickler = pickle.Unpickler(f)
        pwm.workspaces.workspaces = unpickler.load()
        pwm.workspaces.current_workspace_index = unpickler.load()
        pwm.windows.managed = unpickler.load()
        pwm.windows.ignore_unmaps = unpickler.load()
        pwm.windows.handle_focus(unpickler.load())
