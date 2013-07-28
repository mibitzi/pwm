import functools as ft
import pwm.commands as cmd
import pwm.widgets as widgets


class Values():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

loglevel = "debug"

bar = Values(
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

    # Widgets are defined as a list of functions
    # Every widget function should return a tuple like:
    #     (color, text)
    # Where color is a hex value such as #ffffff. If color is None the default
    # foreground color will be used.
    widgets=[
        widgets.time
    ])


window = Values(
    border=2,
    focused="#1793D1",
    unfocused="#222222",
    urgent="#900000")


workspaces = 10

# Keys are described as tuples.
# The first value should be a string describing the key.
# It should start with one or more modifiers following exactly one key.
# Avaliable modifiers are:
#    Control, Shift, Mod1, Mod2, Mod3, Mod4, Mod5
# Whereas Mod4 is usually the Super/Windows key
#
# The second value is the function to execute.
# functools.partial can be used to pass a function with parameters
keys = [
    ("Mod4-Shift-q", cmd.quit),
    ("Mod4-q", cmd.kill),
    ("Mod4-Return", ft.partial(cmd.spawn, "urxvt")),
    ("Mod4-p", ft.partial(cmd.spawn, "dmenu_run"))
]

# Keys for every workspace
for i in range(1, 10):
    keys.append(("Mod4-%d" % i, ft.partial(cmd.switch_workspace, (i-1))))
keys.append(("Mod4-0", ft.partial(cmd.switch_workspace, 9)))
