# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from pwm.config import config
from pwm.ffi.xcb import xcb
import pwm.windows


class Column:
    def __init__(self, size, windows):
        self.size = size
        self.windows = windows


class Window:
    def __init__(self, size, wid):
        self.size = size
        self.wid = wid


class Tiling:
    def __init__(self, workspace):
        self.workspace = workspace
        self.columns = [Column(1.0, [])]

    def add_window(self, wid, column=0, row=-1):
        if column >= len(self.columns):
            self.columns.append(Column(1.0, [Window(1.0, wid)]))
        else:
            num_windows = len(self.columns[column].windows)
            if row == -1:
                row = num_windows

            size = 1.0 / (num_windows+1)
            self.make_row_space(column, size)
            self.columns[column].windows.insert(row, Window(size, wid))

        pwm.windows.configure(wid, stackmode=xcb.STACK_MODE_BELOW)
        self.arrange()

    def remove_window(self, wid):
        column, row = self.path(wid)
        del self.columns[column].windows[row]

        if len(self.columns) > 1 and not self.columns[column].windows:
            # Don't leave empty columns behind
            del self.columns[column]
            self.distribute_free_column_space()
        else:
            self.distribute_free_row_space(column)

        self.arrange()

    def path(self, wid):
        """Find the window and return its column and row.

        Args:
            wid: The window id to find.

        Raises:
            ValueError: The wid was not found.
        """
        for cidx, col in enumerate(self.columns):
            for widx, win in enumerate(col.windows):
                if win.wid == wid:
                    return (cidx, widx)

        raise ValueError

    def move(self, wid, direction):
        getattr(self, "_move_{}".format(direction))(wid)

    def _move_up(self, wid):
        """Move the given window one row up."""

        column, row = self.path(wid)

        if row == 0:
            return

        col = self.columns[column]
        col.windows[row], col.windows[row-1] = (col.windows[row-1],
                                                col.windows[row])

        self.arrange()

    def _move_down(self, wid):
        """Move the given window one row down."""

        column, row = self.path(wid)

        if row == len(self.columns[column].windows) - 1:
            return

        bottom_wid = self.columns[column].windows[row+1].wid
        self._move_up(bottom_wid)

    def _move_left(self, wid):
        self._move_left_right(wid, -1)

    def _move_right(self, wid):
        self._move_left_right(wid, 1)

    def _move_left_right(self, wid, offset):
        col_idx, row = self.path(wid)
        column = self.columns[col_idx]

        move_left = (offset < 0)
        move_right = not move_left

        isleft = (col_idx == 0)
        isright = (col_idx == len(self.columns)-1)
        isoutermost = ((move_left and isleft) or (move_right and isright))

        if len(column.windows) == 1 and isoutermost:
            # If this window is already alone at the left/right, there is
            # no point in going further...
            return
        elif isoutermost:
            # ... but if we share the space with others, we will create a new
            # column for this window alone.
            win = column.windows[row]
            del column.windows[row]
            self.distribute_free_row_space(col_idx)
            win.size = 1.0

            size = 1.0/(len(self.columns)+1)
            self.make_column_space(size)
            self.columns.insert(max(0, col_idx+offset), Column(size, [win]))
        else:
            # In all other cases we just shift the window.
            win = column.windows[row]
            del column.windows[row]
            self.distribute_free_row_space(col_idx)

            win.size = 1.0 / (len(self.columns[col_idx+offset].windows)+1)
            self.make_row_space(col_idx+offset, win.size)
            self.columns[col_idx+offset].windows.append(win)

            # Make sure we don't leave empty columns behind.
            if not column.windows:
                del self.columns[col_idx]
                self.distribute_free_column_space()

        self.arrange()

    def relative(self, wid, pos):
        """Find the window in relative position to this one."""
        return getattr(self, "_relative_{}".format(pos))(wid)

    def _relative_above(self, wid):
        """Find the window above the given wid.

        If this window is the topmost window, return its wid.
        """
        column, row = self.path(wid)
        return wid if row == 0 else self.columns[column].windows[row-1].wid

    def _relative_below(self, wid):
        """Find the window below the given wid.

        If this window is the bottommost window, return its wid.
        """
        column, row = self.path(wid)
        return (wid if row == len(self.columns[column].windows)-1
                else self.columns[column].windows[row+1].wid)

    def _relative_left(self, wid):
        """Find the window left of the given wid.

        If the window is the leftmost window, return its wid.
        """
        column, row = self.path(wid)

        if column == 0:
            return wid
        else:
            left_col = self.columns[column-1]
            return left_col.windows[min(row, len(left_col.windows)-1)].wid

    def _relative_right(self, wid):
        """Find the window right of the given wid.

        If this window is the rightmost window, return its wid.
        """
        column, row = self.path(wid)

        if column == len(self.columns)-1:
            return wid
        else:
            right_col = self.columns[column+1]
            return right_col.windows[min(row, len(right_col.windows)-1)].wid

    def make_row_space(self, column, amount):
        """Make space for a new row by reducing the size of the other rows.

        Args:
            column: The column in which the rows have to be resized.
            amount: The total amount of space to free.
        """
        for win in self.columns[column].windows:
            win.size -= win.size*amount

    def distribute_free_row_space(self, column):
        """Distribute all free space in a column among its rows.

        Args:
            column: The column to check.
        """
        total = sum(w.size for w in self.columns[column].windows)
        amount = 1.0-total

        for win in self.columns[column].windows:
            win.size += amount*win.size/total

    def make_column_space(self, amount):
        """Make space for a new column by shrinking all columns.

        Args:
            amount: The total amount of space to free.
        """
        for col in self.columns:
            col.size -= col.size*amount

    def distribute_free_column_space(self):
        """Distribute all free space among the columns."""
        total = sum(c.size for c in self.columns)
        amount = 1.0-total

        for col in self.columns:
            col.size += amount*col.size/total

    def resize(self, wid, delta):
        """Resize a window by a given delta.

        Args:
            wid: The window to resize.
            delta: A tuple with two values describing change in width and
                   height.
        """
        col_idx, row_idx = self.path(wid)
        dx, dy = delta

        # If there is only one column or only one window in the column
        # then we restrict resizing to prevent empty spaces

        if dx != 0.0 and len(self.columns) > 1:
            column = self.columns[col_idx]
            column.size += dx

            del self.columns[col_idx]
            self.distribute_free_column_space()
            self.make_column_space(column.size)
            self.columns.insert(col_idx, column)

        if dy != 0.0 and len(self.columns[col_idx].windows) > 1:
            window = self.columns[col_idx].windows[row_idx]
            window.size += dy

            del self.columns[col_idx].windows[row_idx]
            self.distribute_free_row_space(col_idx)
            self.make_row_space(col_idx, window.size)
            self.columns[col_idx].windows.insert(row_idx, window)

        self.arrange()

    def arrange(self):
        """Apply layout structure to windows. Use geometry from workspace."""

        left = 0
        for col in self.columns:
            top = 0
            width = round(self.workspace.width*col.size)
            for win in col.windows:
                height = round(self.workspace.height*win.size)
                pwm.windows.configure(win.wid,
                                      x=left,
                                      y=top,
                                      width=width,
                                      height=height)

                top += height
            left += width


class Floating:
    def __init__(self, workspace):
        self.workspace = workspace
        self.windows = []
        self.dirmap = {"up": (0, -1),
                       "down": (0, 1),
                       "left": (-1, 0),
                       "right": (1, 0)}

    def add_window(self, wid):
        self.windows.append(wid)

        x, y, width, height = pwm.windows.preferred_geometry(wid)
        pwm.windows.configure(wid, x=x, y=y, width=width, height=height,
                              stackmode=xcb.STACK_MODE_ABOVE)

    def remove_window(self, wid):
        self.windows.remove(wid)

    def _delta(self, direction, mul):
        return (self.dirmap[direction][0]*mul, self.dirmap[direction][1]*mul)

    def move(self, wid, direction):
        x, y, _, _ = pwm.windows.get_geometry(wid)
        dx, dy = self._delta(direction, config.window.move_speed)

        pwm.windows.configure(wid,
                              x=round(x+self.workspace.width*dx),
                              y=round(y+self.workspace.height*dy))

    def resize(self, wid, delta):
        x, y, width, height = pwm.windows.get_geometry(wid)
        border = config.window.border

        width = max(10, round(width+2*border+self.workspace.width*delta[0]))
        height = max(10, round(height+2*border+self.workspace.height*delta[1]))

        pwm.windows.configure(wid, width=width, height=height)

    def relative(self, wid, pos):
        idx = self.windows.index(wid)+1
        return (self.windows[idx] if idx < len(self.windows)
                else self.windows[0])
