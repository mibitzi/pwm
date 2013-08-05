# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import logging

from pwm.ffi.xcb import xcb
import pwm.xutil

selection_window = None
tray_atom = None

clients = {}

SYSTEM_TRAY_REQUEST_DOCK = 0
SYSTEM_TRAY_BEGIN_MESSAGE = 1
SYSTEM_TRAY_CANCEL_MESSAGE = 2

XEMBED_MAPPED = (1 << 0)
XEMBED_EMBEDDED_NOTIFY = 0


def setup():
    """Setup the system tray.

    Initializes tray support by requesting the appropriate _NET_SYSTEM_TRAY
    atom for the X11 display we are running on, then acquiring the selection
    for this atom. Afterwards, tray clients will send ClientMessages to our
    window.
    """

    # We need a window to own the selection
    global selection_window
    selection_window = pwm.windows.create(
        -1, -1, 1, 1, xcb.mask((xcb.CW_OVERRIDE_REDIRECT, 1)))
    xcb.core.map_window(selection_window)

    # Get the selection
    global tray_atom
    tray_atom = pwm.xutil.get_atom("_NET_SYSTEM_TRAY_S{}".format(
        xcb.screen_number))
    xcb.core.set_selection_owner(selection_window, tray_atom, xcb.CURRENT_TIME)

    # Inform clients waiting for a new _NET_SYSTEM_TRAY that we took the
    # selection.
    event = pwm.windows.create_client_message(
        xcb.screen.root,
        pwm.xutil.get_atom("MANAGER"),
        xcb.CURRENT_TIME,
        tray_atom,
        selection_window)

    xcb.core.send_event(False, xcb.screen.root, 0xffffff, event)


def destroy():
    xcb.core.set_selection_owner(xcb.NONE, tray_atom, xcb.CURRENT_TIME)
    pwm.windows.destroy(selection_window)


def handle_client_message(event):
    """Handle client messages directed at the systray."""

    # System Tray Specification
    # http://standards.freedesktop.org/systemtray-spec/latest
    #
    # The first data field in the message is a timestamp (the stamp of the
    # current event, if available, otherwise CurrentTime). The second data
    # field is an integer indicating the op code of the message.
    # The content remaining three data fields depends on the type of message
    # being sent.

    # To begin the docking process, the tray icon application sends a
    # client message event to the manager selection owner window, [...].
    # This event should contain the SYSTEM_TRAY_REQUEST_DOCK opcode,
    # xclient.data.l[2] should contain the X window ID of the tray icon to be
    # docked.

    # At this point the "embedding life cycle" explained in the XEMBED
    # specification begins. The XEMBED specification explains how the
    # embedding application will interact with the embedded tray icon, and how
    # the embedder/embedded relationship may be ended.

    if event.data.data32[1] == SYSTEM_TRAY_REQUEST_DOCK:
        client = event.data.data32[2]
        logging.debug("client {} requested docking".format(client))

        # Listen for PropertyNotify events to get the most recent value of
        # the XEMBED_MAPPED atom, also listen for UnmapNotify events
        pwm.windows.change_attributes(
            client, (xcb.CW_EVENT_MASK,
                     xcb.EVENT_MASK_PROPERTY_CHANGE |
                     xcb.EVENT_MASK_STRUCTURE_NOTIFY))

        # Request the _XEMBED_INFO property. The XEMBED specification
        # says this *has* to be set, but VLC does not set it...
        xe_version = 1
        map_it = True
        info = pwm.xutil.get_property_value(
            pwm.xutil.get_property(client, "_XEMBED_INFO").reply())

        if info:
            xe_version = info[0]
            map_it = ((info[1] & XEMBED_MAPPED) == XEMBED_MAPPED)
            logging.debug("xembed version: {}".format(info[0]))
            logging.debug("xembed flags: {}".format(info[1]))
        else:
            logging.debug("client {} violates the XEMBED protocol, "
                          "_XEMBED_INFO not set.".format(client))

        # Put the client inside the save set. Upon termination (whether killed
        # or normal exit does not matter), these clients will be correctly
        # reparented to their most closest living ancestor. Without this, tray
        # icons might die when we exit/crash.
        xcb.core.change_save_set(xcb.SET_MODE_INSERT, client)

        xcb.core.reparent_window(client, pwm.bar.primary.wid, 0, 0)

        # We reconfigure the window to use a reasonable size. The systray
        # specification explicitly says:
        #   Tray icons may be assigned any size by the system tray, and
        #   should do their best to cope with any size effectively
        size = pwm.bar.primary.height
        xcb.core.configure_window(
            client, *xcb.mask([(xcb.CONFIG_WINDOW_WIDTH, size),
                               (xcb.CONFIG_WINDOW_HEIGHT, size)]))

        # Send the XEMBED_EMBEDDED_NOTIFY message.
        # http://standards.freedesktop.org/xembed-spec/xembed-spec-latest.html
        # An XEmbed message is an X11 client message with message type
        # "_XEMBED". The format is 32, the first three data longs carry the
        # toolkit's X time (l[0]), the message's major opcode (l[1]) and the
        # message's detail code (l[2]). If no detail is required, the value
        # passed has to be 0. The remaining two data longs (l[3] and l[4]) are
        # reserved for data1 and data2. Unused bytes of the client message are
        # set to 0. The event is sent to the target window with no event mask
        # and propagation turned off.
        event = pwm.windows.create_client_message(
            client,
            pwm.xutil.get_atom("_XEMBED"),
            xcb.CURRENT_TIME,
            XEMBED_EMBEDDED_NOTIFY,
            0,
            pwm.bar.primary.wid,
            xe_version)

        xcb.core.send_event(False, client, xcb.EVENT_MASK_NO_EVENT, event)

        if map_it:
            xcb.core.map_window(client)

        clients[client] = map_it

        configure_clients()


def configure_clients():
    offset = 0
    for client, mapped in clients.items():
        if not mapped:
            continue

        offset += pwm.bar.primary.height+2
        xcb.core.configure_window(
            client,
            *xcb.mask((xcb.CONFIG_WINDOW_X, pwm.bar.primary.width-offset)))

    pwm.bar.primary.update_systray(offset)


def handle_unmap(wid):
    del clients[wid]
    configure_clients()


def handle_property_notify(event):
    if (event.atom != pwm.xutil.get_atom("_XEMBED_INFO") or
            event.state != xcb.PROPERTY_NEW_VALUE):
        return

    client = event.window

    info = pwm.xutil.get_property_value(
        pwm.xutil.get_property(client, "_XEMBED_INFO").reply())

    if not info:
        return

    map_it = ((info[1] & XEMBED_MAPPED) == XEMBED_MAPPED)
    mapped = clients[client]

    if not mapped and map_it:
        xcb.core.map_window(client)
    elif mapped and not map_it:
        xcb.core.map_window(client)

    clients[client] = map_it
    configure_clients()
