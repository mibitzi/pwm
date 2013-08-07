import pwm.commands as cmd
import pwm.widgets as widgets


class Values():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


loglevel = "debug"

bar = Values(
    interval=1.0,
    font=Values(face="DejaVu Sans Mono", size=12),

    background="#222222",
    foreground="#ffffff",

    active_workspace_foreground="#ffffff",
    active_workspace_background="#285577",
    active_workspace_border="#4c7899",

    inactive_workspace_foreground="#888888",
    inactive_workspace_background="#222222",
    inactive_workspace_border="#333333",

    urgent_workspace_foreground="#ffffff",
    urgent_workspace_background="#900000",
    urgent_workspace_border="#2f343a",

    # Widgets are defined as a list of functions.
    # Every widget function should return a tuple like:
    #     (color, text)
    # Where color is a hex value string such as "#ffffff".
    # If color is None the default foreground color will be used.
    widgets=[
        widgets.volume(),
        widgets.separator(),
        widgets.battery("BAT1"),
        widgets.separator(),
        widgets.disk("/"),
        widgets.separator(),
        widgets.disk("/home"),
        widgets.separator(),
        widgets.load(),
        widgets.separator(),
        widgets.time(),
    ])


window = Values(
    border=2,
    focused="#1793D1",
    unfocused="#222222",
    urgent="#900000",

    # How fast should floating windows move
    move_speed=0.02)


workspaces = 10

# Keys are described as tuples.
# The first value should be a string describing the key.
# It should start with one or more modifiers following exactly one key.
# Avaliable modifiers are:
#    Control, Shift, Mod1, Mod2, Mod3, Mod4, Mod5
# Whereas Mod4 is usually the Super/Windows key
#
# The second value is the function to execute.
keys = [
    ("Mod4-Shift-q", cmd.quit()),
    ("Mod4-Shift-r", cmd.restart()),
    ("Mod4-q", cmd.kill()),
    ("Mod4-Return", cmd.spawn("urxvt")),
    ("Mod4-p", cmd.menu()),
    ("Mod4-f", cmd.toggle_floating()),
    ("Mod4-space", cmd.toggle_focus_layer()),

    ("Mod4-h", cmd.focus("left")),
    ("Mod4-j", cmd.focus("below")),
    ("Mod4-k", cmd.focus("above")),
    ("Mod4-l", cmd.focus("right")),

    ("Shift-Mod4-h", cmd.move("left")),
    ("Shift-Mod4-j", cmd.move("down")),
    ("Shift-Mod4-k", cmd.move("up")),
    ("Shift-Mod4-l", cmd.move("right")),

    ("Control-Mod4-h", cmd.resize((-0.02, 0))),
    ("Control-Mod4-j", cmd.resize((0, 0.02))),
    ("Control-Mod4-k", cmd.resize((0, -0.02))),
    ("Control-Mod4-l", cmd.resize((0.02, 0))),

    ("XF86AudioRaiseVolume", cmd.spawn("amixer -q set Master 2dB+ unmute")),
    ("XF86AudioLowerVolume", cmd.spawn("amixer -q set Master 2dB- unmute")),
    ("XF86AudioMute", cmd.spawn("amixer -q set Master toggle")),

    ("XF86MonBrightnessUp", cmd.spawn("/usr/bin/xbacklight -inc 10")),
    ("XF86MonBrightnessDown", cmd.spawn("/usr/bin/xbacklight -dec 10")),
]

# Keys for every workspace.
# Note that workspace indices are zero-based.
for i in range(9):
    keys.append(("Mod4-{}".format(i+1), cmd.switch_workspace(i)))
    keys.append(("Shift-Mod4-{}".format(i+1), cmd.send_to_workspace(i)))
keys.append(("Mod4-0", cmd.switch_workspace(9)))
keys.append(("Shift-Mod4-0", cmd.send_to_workspace(9)))
