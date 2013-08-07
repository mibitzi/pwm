# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import pwm.windows
import pwm.workspaces
import pwm.menu
import pwm.spawn
import pwm.worker
import pwm.events
import pwm.main
import pwm.config


@pwm.config.create_arguments
def quit():
    """Exit pwm."""
    pwm.events.shutdown = True


@pwm.config.create_arguments
def restart():
    """Restart pwm."""
    pwm.events.shutdown = True
    pwm.main.restart = True


@pwm.config.create_arguments
def switch_workspace(index):
    """Switch to given workspace.

    Workspace indices are zero-based.
    """
    pwm.workspaces.switch(index)


@pwm.config.create_arguments
@pwm.windows.only_if_focused
def kill(focused, ws):
    """Kill the currently active window."""
    pwm.windows.kill(focused)


@pwm.config.create_arguments
def spawn(cmd):
    pwm.spawn.spawn(cmd)


@pwm.config.create_arguments
@pwm.windows.only_if_focused
def move(focused, ws, direction):
    """Move the currently focused window in the given direction.

    Args:
        direction: Can be "up", "down", "left" or "right"
    """
    ws.move_window(focused, direction)


@pwm.config.create_arguments
@pwm.windows.only_if_focused
def focus(focused, ws, pos):
    """Focus another window.

    Args:
        pos: Can be "above", "below", "left" or "right"
    """
    ws.focus_relative(focused, pos)


@pwm.config.create_arguments
@pwm.windows.only_if_focused
def resize(focused, ws, delta):
    """Resize the currently focused window.

    Args:
        delta: A tuple with two values indicating the change in width and
               height.
    """
    ws.resize_window(focused, delta)


@pwm.config.create_arguments
@pwm.windows.only_if_focused
def send_to_workspace(focused, ws, workspace):
    """Send the currently focused window to another workspace.

    Args:
        workspace: A workspace index
    """
    pwm.workspaces.send_window_to(focused, workspace)


@pwm.config.create_arguments
@pwm.windows.only_if_focused
def toggle_floating(focused, ws):
    """Toggle the floating mode for a window on/off."""
    ws.toggle_floating(focused)


@pwm.config.create_arguments
@pwm.windows.only_if_focused
def toggle_focus_layer(focused, ws):
    """Toggle focus tiling/floating windows."""
    ws.toggle_focus_layer()


@pwm.config.create_arguments
def menu():
    """Show the application menu."""
    pwm.menu.show()
