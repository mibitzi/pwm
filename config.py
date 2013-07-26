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


keys = [
    Key("Mod4-a", cmd.kill),
    Key("Mod4-x", cmd.quit)
]


for i in range(1, 10):
    keys.append(Key("Mod4-%d" % i, cmd.switch_workspace, (i-1)))
keys.append(Key("Mod4-0", cmd.switch_workspace, 9))
