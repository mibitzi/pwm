from pwm.config import Key
import pwm.commands as cmd


class Values(dict):
    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__.update(kw)

loglevel = "debug"

bar = Values(
    height=18,
    background="#222222",
    foreground="#ffffff",
    font=Values(face="DejaVu Sans Mono", size=12))

window = Values(
    border=3,
    focused="#1793D1",
    unfocused="#222222",
    urgent="#900000")

workspaces = 10

keys = [
    Key("Mod4-q", cmd.quit)
]

for i in range(1, 10):
    keys.append(Key("Mod4-%d" % i, cmd.switch_workspace, i-1))
