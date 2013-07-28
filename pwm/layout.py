# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.windows


class Column:
    def __init__(self, size, windows):
        self.size = size
        self.windows = windows


class Window:
    def __init__(self, size, wid):
        self.size = size
        self.wid = wid


class Layout:
    def __init__(self, workspace):
        self.columns = [Column(1.0, [])]
        self.workspace = workspace

    def add_window(self, wid, column=0, row=-1):
        if column >= len(self.columns):
            self.columns.append(Column(1.0, [Window(1.0, wid)]))
        else:
            if row == -1:
                row = len(self.columns[column].windows)
            self.columns[column].windows.insert(row, Window(1.0, wid))

        self.arrange()

    def remove_window(self, wid):
        column, row = self.path(wid)
        del self.columns[column].windows[row]

        # Don't leave empty columns behind
        if len(self.columns) > 1 and not self.columns[column].windows:
            del self.columns[column]

        self.arrange()

    def path(self, wid):
        """Find the window and return its column and row."""
        for cidx, col in enumerate(self.columns):
            for widx, win in enumerate(col.windows):
                if win.wid == wid:
                    return (cidx, widx)

        raise ValueError

    def move_up(self, wid):
        """Move the given window one row up."""

        column, row = self.path(wid)

        if row == 0:
            return

        col = self.columns[column]
        col.windows[row], col.windows[row-1] = (col.windows[row-1],
                                                col.windows[row])

        self.arrange()

    def move_down(self, wid):
        """Move the given window one row down."""

        column, row = self.path(wid)

        if row == len(self.columns[column].windows) - 1:
            return

        bottom_wid = self.columns[column].windows[row+1].wid
        self.move_up(bottom_wid)

    def move_left(self, wid):
        col_idx, row = self.path(wid)
        column = self.columns[col_idx]

        if col_idx == 0 and len(column.windows) == 1:
            # If this window is already alone on the left do nothing.
            return
        elif col_idx == 0:
            # If this window is in the first column with others,
            # create a new column at the beginning with this window in it.
            win = column.windows[row]
            del column.windows[row]
            self.columns.insert(col_idx, Column(1.0, [win]))
        else:
            # Otherwise move this window to the column on the left.
            win = column.windows[row]
            del column.windows[row]
            self.columns[col_idx-1].windows.append(win)

            # Make sure we don't leave empty columns behind.
            if not column.windows:
                del self.columns[col_idx]

        self.arrange()

    def move_right(self, wid):
        col_idx, row = self.path(wid)
        column = self.columns[col_idx]

        if col_idx == len(self.columns)-1 and len(column.windows) == 1:
            # If this window is already alone on the right do nothing.
            return
        elif col_idx == len(self.columns)-1:
            # If this window is in the last column with others,
            # create a new column at the end with this window in it.
            win = column.windows[row]
            del column.windows[row]
            self.columns.append(Column(1.0, [win]))
        else:
            # Otherwise move this window to the column on the right.
            win = column.windows[row]
            del column.windows[row]
            self.columns[col_idx+1].windows.append(win)

            # Make sure we don't leave empty columns behind.
            if not column.windows:
                del self.columns[col_idx]

        self.arrange()

    def above(self, wid):
        """Find the window above the given wid.

        If this window is the topmost window, return its wid.
        """
        column, row = self.path(wid)
        return wid if row == 0 else self.columns[column].windows[row-1].wid

    def below(self, wid):
        """Find the window below the given wid.

        If this window is the bottommost window, return its wid.
        """
        column, row = self.path(wid)
        return (wid if row == len(self.columns[column].windows)-1
                else self.columns[column].windows[row-1].wid)

    def left(self, wid):
        """Find the window left of the given wid.

        If the window is the leftmost window, return its wid.
        """
        column, row = self.path(wid)

        if column == 0:
            return wid
        else:
            left_col = self.columns[column-1]
            return left_col.windows[min(row, len(left_col.windows)-1)].wid

    def right(self, wid):
        """Find the window right of the given wid.

        If this window is the rightmost window, return its wid.
        """
        column, row = self.path(wid)

        if column == len(self.columns)-1:
            return wid
        else:
            right_col = self.columns[column+1]
            return right_col.windows[min(row, len(right_col.windows)-1)].wid

    def arrange(self):
        """Apply layout structure to windows. Use geometry from workspace."""

        for col in self.columns:
            col.size = round(1.0 / len(self.columns), 3)

            for win in col.windows:
                win.size = round(1.0 / len(col.windows), 3)

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
