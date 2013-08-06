# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from collections import defaultdict
import re

from pwm.ffi.xcb import xcb
from pwm.ffi.xcb import XcbError
from pwm.keysyms import keysyms, keysym_strings

#
# Based on xpybutil
# https://github.com/BurntSushi/xpybutil/blob/master/xpybutil/keybind.py
#

__kbmap = None
__keysmods = None

__keybinds = defaultdict(list)

TRIVIAL_MODS = [
    0,
    xcb.MOD_MASK_LOCK,
    xcb.MOD_MASK_2,
    xcb.MOD_MASK_LOCK | xcb.MOD_MASK_2
]


def strip_trivial(mods):
    """Strip out all trivial mods."""

    for mod in TRIVIAL_MODS:
        mods &= ~mod

    return mods


def parse_keystring(key_string):
    """
    A utility function to turn strings like 'Mod1-Mod4-a' into a pair
    corresponding to its modifiers and keycode.

    :param key_string: String starting with zero or more modifiers followed
                       by exactly one key press.

                       Available modifiers: Control, Mod1, Mod2, Mod3, Mod4,
                       Mod5, Shift, Lock
    :type key_string: str
    :return: Tuple of modifier mask and keycode
    :rtype: (mask, int)
    """
    modifiers = 0
    keycode = None

    for part in key_string.split('-'):
        try:
            xcb_part = part.upper()
            xcb_part = re.sub(r"(.)([0-9])", r"\1_\2", xcb_part)
            modifiers |= getattr(xcb, "KEY_BUT_MASK_%s" % xcb_part)
            continue
        except:
            pass

        if len(part) == 1:
            part = part.lower()
        keycode = lookup_string(part)

    return modifiers, keycode


def lookup_string(kstr):
    """
    Finds the keycode associated with a string representation of a keysym.

    :param kstr: English representation of a keysym.
    :return: Keycode, if one exists.
    :rtype: int
    """
    if kstr in keysyms:
        return get_keycode(keysyms[kstr])
    elif len(kstr) > 1 and kstr.capitalize() in keysyms:
        return get_keycode(keysyms[kstr.capitalize()])

    return None


def get_min_max_keycode():
    """
    Return a tuple of the minimum and maximum keycode allowed in the
    current X environment.

    :rtype: (int, int)
    """
    return (xcb.setup.min_keycode, xcb.setup.max_keycode)


def get_keyboard_mapping():
    """
    Return a keyboard mapping cookie that can be used to fetch the table of
    keysyms in the current X environment.

    :rtype: xcb.xproto.GetKeyboardMappingCookie
    """
    mn, mx = get_min_max_keycode()

    return xcb.core.get_keyboard_mapping(mn, mx - mn + 1)


def get_keysym(keycode, col=0, kbmap=None):
    """
    Get the keysym associated with a particular keycode in the current X
    environment. Although we get a list of keysyms from X in
    'get_keyboard_mapping', this list is really a table with
    'keysys_per_keycode' columns and ``mx - mn`` rows (where ``mx`` is the
    maximum keycode and ``mn`` is the minimum keycode).

    Thus, the index for a keysym given a keycode is:
    ``(keycode - mn) * keysyms_per_keycode + col``.

    In most cases, setting ``col`` to 0 will work.

    Witness the utter complexity:
    http://tronche.com/gui/x/xlib/input/keyboard-encoding.html

    You may also pass in your own keyboard mapping using the ``kbmap``
    parameter, but xpybutil maintains an up-to-date version of this so you
    shouldn't have to.

    :param keycode: A physical key represented by an integer.
    :type keycode: int
    :param col: The column in the keysym table to use.
                Unless you know what you're doing, just use 0.
    :type col: int
    :param kbmap: The keyboard mapping to use.
    :type kbmap: xcb.xproto.GetKeyboardMapingReply
    """
    if kbmap is None:
        kbmap = __kbmap

    mn, mx = get_min_max_keycode()
    per = kbmap.keysyms_per_keycode
    ind = (keycode - mn) * per + col

    return xcb.get_keyboard_mapping_keysyms(kbmap)[ind]


def get_keysym_string(keysym):
    """
    A simple wrapper to find the english string associated with a particular
    keysym.

    :param keysym: An X keysym.
    :rtype: str
    """
    return keysym_strings.get(keysym, [None])[0]


def get_keycode(keysym):
    """
    Given a keysym, find the keycode mapped to it in the current X environment.
    It is necessary to search the keysym table in order to do this, including
    all columns.

    :param keysym: An X keysym.
    :return: A keycode or None if one could not be found.
    :rtype: int
    """
    mn, mx = get_min_max_keycode()
    cols = __kbmap.keysyms_per_keycode
    for i in range(mn, mx + 1):
        for j in range(0, cols):
            ks = get_keysym(i, col=j)
            if ks == keysym:
                return i

    return None


def get_mod_for_key(keycode):
    """
    Finds the modifier that is mapped to the given keycode.
    This may be useful when analyzing key press events.

    :type keycode: int
    :return: A modifier identifier.
    :rtype: xcb.xproto.ModMask
    """
    return __keysmods.get(keycode, 0)


def get_keys_to_mods():
    """
    Fetches and creates the keycode -> modifier mask mapping. Typically, you
    shouldn't have to use this---xpybutil will keep this up to date if it
    changes.

    This function may be useful in that it should closely replicate the output
    of the ``xmodmap`` command. For example:

     ::

        keymods = get_keys_to_mods()
        for kc in sorted(keymods, key=lambda kc: keymods[kc]):
            print keymods[kc], hex(kc), get_keysym_string(get_keysym(kc))

    Which will very closely replicate ``xmodmap``. I'm not getting precise
    results quite yet, but I do believe I'm getting at least most of what
    matters. (i.e., ``xmodmap`` returns valid keysym strings for some that
    I cannot.)

    :return: A dict mapping from keycode to modifier mask.
    :rtype: dict
    """
    modmasks = [xcb.MOD_MASK_SHIFT, xcb.MOD_MASK_LOCK, xcb.MOD_MASK_CONTROL,
                xcb.MOD_MASK_1, xcb.MOD_MASK_2, xcb.MOD_MASK_3,
                xcb.MOD_MASK_4, xcb.MOD_MASK_5]  # order matters

    mods = xcb.core.get_modifier_mapping().reply()

    res = {}
    keyspermod = mods.keycodes_per_modifier
    keycodes = xcb.get_modifier_mapping_keycodes(mods)
    for mmi in range(0, len(modmasks)):
        row = mmi * keyspermod
        for kc in keycodes[row:row + keyspermod]:
            res[kc] = modmasks[mmi]

    return res


def get_modifiers(state):
    """
    Takes a ``state`` (typically found in key press or button press events)
    and returns a string list representation of the modifiers that were pressed
    when generating the event.

    :param state: Typically from ``some_event.state``.
    :return: List of modifier string representations.
    :rtype: [str]
    """
    ret = []

    if state & xcb.MOD_MASK_SHIFT:
        ret.append('Shift')
    if state & xcb.MOD_MASK_LOCK:
        ret.append('Lock')
    if state & xcb.MOD_MASK_CONTROL:
        ret.append('Control')
    if state & xcb.MOD_MASK_1:
        ret.append('Mod1')
    if state & xcb.MOD_MASK_2:
        ret.append('Mod2')
    if state & xcb.MOD_MASK_3:
        ret.append('Mod3')
    if state & xcb.MOD_MASK_4:
        ret.append('Mod4')
    if state & xcb.MOD_MASK_5:
        ret.append('Mod5')
    if state & xcb.KEY_BUT_MASK_BUTTON1:
        ret.append('Button1')
    if state & xcb.KEY_BUT_MASK_BUTTON2:
        ret.append('Button2')
    if state & xcb.KEY_BUT_MASK_BUTTON3:
        ret.append('Button3')
    if state & xcb.KEY_BUT_MASK_BUTTON4:
        ret.append('Button4')
    if state & xcb.KEY_BUT_MASK_BUTTON5:
        ret.append('Button5')

    return ret


def grab_key(wid, modifiers, key):
    """
    Grabs a key for a particular window and a modifiers/key value.
    If the grab was successful, return True. Otherwise, return False.
    If your client is grabbing keys, it is useful to notify the user if a
    key wasn't grabbed. Keyboard shortcuts not responding is disorienting!

    Also, this function will grab several keys based on varying modifiers.
    Namely, this accounts for all of the "trivial" modifiers that may have
    an effect on X events, but probably shouldn't effect key grabbing. (i.e.,
    whether num lock or caps lock is on.)

    N.B. You should probably be using 'bind_key' or 'bind_global_key' instead.

    :param wid: A window identifier.
    :type wid: int
    :param modifiers: A modifier mask.
    :type modifiers: int
    :param key: A keycode.
    :type key: int
    :rtype: bool
    """
    try:
        for mod in TRIVIAL_MODS:
            xcb.core.grab_key_checked(True, wid,
                                      modifiers | mod, key,
                                      xcb.GRAB_MODE_ASYNC,
                                      xcb.GRAB_MODE_ASYNC).check()

        return True
    except XcbError:
        return False


def ungrab_key(wid, modifiers, key):
    """
    Ungrabs a key that was grabbed by ``grab_key``. Similarly, it will return
    True on success and False on failure.

    When ungrabbing a key, the parameters to this function should be
    *precisely* the same as the parameters to ``grab_key``.

    :param wid: A window identifier.
    :type wid: int
    :param modifiers: A modifier mask.
    :type modifiers: int
    :param key: A keycode.
    :type key: int
    :rtype: bool
    """
    try:
        for mod in TRIVIAL_MODS:
            xcb.core.ungrab_key_checked(key, wid, modifiers | mod).check()
        return True
    except XcbError:
        return False


def update_keyboard_mapping(e=None):
    """
    Whenever the keyboard mapping is changed, this function needs to be called
    to update xpybutil's internal representing of the current keysym table.
    Indeed, xpybutil will do this for you automatically.

    Moreover, if something is changed that affects the current keygrabs,
    xpybutil will initiate a regrab with the changed keycode.

    :param e: The MappingNotify event.
    :type e: xcb.xproto.MappingNotifyEvent
    :rtype: void
    """
    global __kbmap, __keysmods

    newmap = get_keyboard_mapping().reply()

    if e is None:
        __kbmap = newmap
        __keysmods = get_keys_to_mods()
        return

    if e.request == xcb.MAPPING_KEYBOARD:
        changes = {}
        for kc in range(*get_min_max_keycode()):
            knew = get_keysym(kc, kbmap=newmap)
            oldkc = get_keycode(knew)
            if oldkc != kc:
                changes[oldkc] = kc

        __kbmap = newmap
        __regrab(changes)
    elif e.request == xcb.MAPPING_MODIFIER:
        __keysmods = get_keys_to_mods()


def __regrab(changes):
    """
    Takes a dictionary of changes (mapping old keycode to new keycode) and
    regrabs any keys that have been changed with the updated keycode.

    :param changes: Mapping of changes from old keycode to new keycode.
    :type changes: dict
    :rtype: void
    """
    for wid, mods, kc in __keybinds:
        if kc in changes:
            ungrab_key(wid, mods, kc)
            grab_key(wid, mods, changes[kc])

            old = (wid, mods, kc)
            new = (wid, mods, changes[kc])
            __keybinds[new] = __keybinds[old]
            del __keybinds[old]
