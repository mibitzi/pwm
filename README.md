Pointless Window Manager
========================
PWM is a simplistic tiling window manager written in python 3.

Dependencies
------------
Package names on Arch Linux:
  - extra/python3
  - aur/python-cffi
  - extra/libxcb
  - extra/xcb-util
  - extra/cairo

Installation
------------
There is an [AUR package][aur] available for Arch Linux.

Alternative installation from source:
```
git checkout git://github.com/mibitzi/pwm.git
cd pwm
python setup.py install
```

Layout
------
In pwm windows can in one of three different states: tiling (default), floating or fullscreen.
Tiling windows will be arranged in a column-based layout in which all windows can be resized freely.

```
---------------------
|        |          |
|________|          |
|        |          |
|        |__________|
|________|          |
|        |          |
---------------------
```

There can be a variable number of columns and every column can have variable amount of rows.
Changing the size of a column will cause the other columns to resize accordingly, same goes with rows.

Configuration
-------------
Unless the config file already exists the default configuration will be copied to `~/.config/pwm/pwmrc.py`.

Default shortcuts
-----------------
Shortcuts are all defined in the config file.
To get started, some important default shortcuts:
  - `Mod4-p` to show the menu to start other applications
  - `Mod4-q` close the focused window
  - `Mod4-Return` start urxvt
  - `Mod4-shift-q` Quit pwm
  - `Mod4-shift-r` Restart pwm
  - ...

[aur]: [https://aur.archlinux.org/packages/pwm-git]
