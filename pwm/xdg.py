# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import os
import glob
import re

# The directories are defined in:
# http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html


def config_home():
    """Return the XDG_CONFIG_HOME directory."""
    return os.getenv("XDG_CONFIG_HOME", os.environ["HOME"]+"/.config")


def data_home():
    """Return the XDG_DATA_HOME directory."""
    return os.getenv("XDG_DATA_HOME", os.environ["HOME"] + "/.local/share")


def data_dirs():
    """Return the XDG_DATA_DIRS directory."""
    return os.getenv("XDG_DATA_DIRS", "/usr/local/share:/usr/share")


def desktop_file_dirs():
    """Return a list of directories in which .desktop files could be stored."""

    search_dirs = [data_home() + "/applications"]
    search_dirs.extend(d + "/applications" for d in data_dirs().split(":"))

    return search_dirs


def find_desktop_files():
    """Find and return a list of all .desktop files for the current user."""
    files = []
    for d in desktop_file_dirs():
        files.extend(glob.glob(os.path.join(d, "*.desktop")))

    return files


def parse_desktop_file(contents):
    """Parse the given .desktop file and return its Name and Exec entries."""

    # The specification for .desktop files can be found at:
    # http://standards.freedesktop.org/desktop-entry-spec/latest

    return {"name": _desktop_file_key(contents, "Name"),
            "exec": _desktop_file_key(contents, "Exec")}


def _desktop_file_key(contents, key):
    match = re.search("^"+key+"\s*=\s*(.*?)$", contents, re.MULTILINE)
    if not match:
        raise ValueError("Desktop file has no {} key".format(key))
    return match.group(1)


def applications():
    """Return a list of all applications found via .desktop files."""

    applications = []
    for path in find_desktop_files():
        with open(path) as f:
            applications.append(parse_desktop_file(f.read()))

    return applications
