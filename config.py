from pwm.config import Key
import pwm.commands as cmd


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
    urgent_workspace_border="#2f343a")


window = Values(
    border=2,
    focused="#1793D1",
    unfocused="#222222",
    urgent="#900000")


workspaces = 10

# The first argument should be a string describing the key.
# It should start with one or more modifiers following exactly one key.
# Avaliable modifiers are:
#    Control, Shift, Mod1, Mod2, Mod3, Mod4, Mod5
# Whereas Mod4 is usually the Super/Windows key
#
# The second argument is the function to execute.
# All following arguments will be passed to that function.
keys = [
    Key("Mod4-Shift-q", cmd.quit),
    Key("Mod4-q", cmd.kill),
    Key("Mod4-Return", cmd.spawn, "urxvt"),
    Key("Mod4-p", cmd.spawn, "dmenu_run")
]


for i in range(1, 10):
    keys.append(Key("Mod4-%d" % i, cmd.switch_workspace, (i-1)))
keys.append(Key("Mod4-0", cmd.switch_workspace, 9))
