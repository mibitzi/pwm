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

keys = [
    Key("Mod4-q", cmd.quit)
]
