"""
===========================================================================
 µnleashed BBS guides
===========================================================================
File:         shots/capture/capture.py
Purpose:      Drive the firmware's host build through every screen the
              guides show, and save the raw session with the offset at
              which each screen is finished. capture.sh runs it; tojson.py
              turns what it saves into shots/*.json.

Usage:        capture.py <firmware checkout> <capture dir> <port> <mode>
                mode  setup   a fresh board: the first login as the sysop
                      config  CONFIG's pages and the callers' views, at 80
                              columns and again at 40
                      camera  a camera board's pages, at 80 columns

Nothing here talks to anything but 127.0.0.1. Each mode is a list of
scenes: a name, the keys that bring the screen up, how long it takes to
draw, and the keys that leave it. A scene that does not draw what it
expects is still saved, and tojson.py says which.

Copyright 2026 - Robert Mech
License:      GNU General Public License v3 or later
SPDX-License-Identifier: GPL-3.0-or-later
===========================================================================
"""
import json
import os
import sys

FW, OUT, PORT, MODE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
sys.argv = ["capture", "127.0.0.1", PORT]
sys.path.insert(0, os.path.join(FW, "tools"))
import testclient as tc  # noqa: E402

SYSOP_PW = "docshots"
ESC = b"\x1b"
CLS = b"cls\r"

# (name, keys, seconds to draw, keys to leave). "cls" first, so each screen
# starts on a clear glass and the capture is the screen and nothing else.
CONFIG_SCENES = [
    ("config-list", CLS + b"config\r", 2.5, None),
    ("config-board", CLS + b"config board\r", 2.5, ESC),
    ("config-limits", CLS + b"config limits\r", 2.5, ESC),
    ("config-accounts", CLS + b"config accounts\r", 2.5, ESC),
    ("config-backup", CLS + b"config backup\r", 2.5, ESC),
    ("config-staff", CLS + b"config staff\r", 2.5, ESC),
    ("config-network", CLS + b"config network\r", 2.5, ESC),
    ("config-chat", CLS + b"config chat\r", 2.5, ESC),
    ("config-forums", CLS + b"config forums\r", 2.5, ESC),
    ("config-info", CLS + b"config info\r", 2.5, ESC),
    ("config-announce", CLS + b"config announce\r", 2.5, ESC),
    ("config-sd", CLS + b"config sd\r", 2.5, ESC),
    ("config-lights", CLS + b"config lights\r", 2.5, ESC),
    ("config-files", CLS + b"config files\r", 2.5, None),
    # Down to Area 1 and open it: the row is a button, the parts a page.
    ("config-area", tc.DOWN * 4 + b"\r", 2.5, ESC + ESC),
    # What a caller sees.
    ("chat-room", CLS + b"chat\r", 3.0, None),
    ("chat-line", b"Anyone on tonight?\r", 2.0, b"/q\r"),
    ("forums-list", CLS + b"forums\r", 3.0, b"q"),
    ("info-list", CLS + b"info\r", 2.5, None),
]
# An ESP32-S3 board (the Waveshare 4.3B's host build): SSH's port, and the
# host keys' fingerprints at the foot of SYS.
S3_SCENES = [
    ("s3-config-network", CLS + b"config network\r", 2.5, ESC),
    ("s3-config-list", CLS + b"config\r", 2.5, None),
    ("s3-hardware", CLS + b"hardware\r", 3.0, b"q"),
]
CAMERA_SCENES = [
    ("config-camera", CLS + b"config camera\r", 2.5, ESC),
    ("config-photos", CLS + b"config photos\r", 2.5, ESC),
    ("snapshot", CLS + b"snapshot\r", 12.0, None),
]


def caller(cols):
    c = tc.Caller(ansi=True, utf8=True)
    # The window size before the board says anything, as a terminal that
    # speaks NAWS does.
    c.s.sendall(b"\xff\xfb\x1f\xff\xfa\x1f\x00" + bytes([cols]) + b"\x00\x18\xff\xf0")
    c.wait_for(b"Enter your handle", 12)
    return c


def run(scenes, cols, tag):
    c = caller(cols)
    print(tag, "login", tc.login(c, "Sparks"))
    c.send(b"bye " + SYSOP_PW.encode() + b"\r")
    c.wait_for(b"Sysop", 8)
    c.pump(1.5)
    marks = {}
    for name, keys, settle, leave in scenes:
        c.send(keys)
        c.pump(settle)
        marks[name] = len(c.buf)
        if leave is not None:
            c.send(leave)
            c.pump(1.5)
    save(c, tag, cols, marks)
    c.send(b"g\r")
    c.pump(1.0)
    c.close()


def save(c, tag, cols, marks):
    with open(os.path.join(OUT, tag + ".bin"), "wb") as fh:
        fh.write(bytes(c.buf))
    with open(os.path.join(OUT, tag + ".json"), "w") as fh:
        json.dump({"cols": cols, "marks": marks}, fh)
    print(tag, "bytes", len(c.buf), sorted(marks))


def page_until(c, text, tries=8):
    """Press SPACE through page breaks until text is on the screen."""
    for _ in range(tries):
        if text in tc.plain(c.buf):
            return True
        p = tc.plain(c.buf)
        if b"Press SPACE" in p or b"PRESS SPACE" in p:
            c.send(b" ")
        c.pump(1.0)
    return text in tc.plain(c.buf)


def setup():
    """A fresh board: the offer, the setup screen, the staff form, the tour."""
    cols = 80
    c = caller(cols)
    print("setup", "registered", tc.login(c, "Sparks", wait_main=False))
    marks = {}
    print("offer", c.wait_for(b"Sysop password", 10))
    c.pump(1.0)
    marks["setup-offer"] = len(c.buf)
    c.send(b"unleashed\r")
    print("staff form", page_until(c, b"STAFF PASSWORDS"))
    c.pump(1.5)
    marks["setup-staff"] = len(c.buf)
    # The setup screen plays and the form clears it at once, so it is never
    # on the glass when a capture could be taken. Its end is the form's own
    # clear screen: everything before that is the setup screen as drawn.
    form = bytes(c.buf).find(b"STAFF PASSWORDS", marks["setup-offer"])
    marks["setup-screen"] = bytes(c.buf).rfind(b"\x1b[2J", marks["setup-offer"], form)
    c.send(b"fresh1234" + tc.F1)
    print("tour", c.wait_for(b"SETTING UP YOUR BOARD", 10))
    c.pump(2.0)
    marks["newsysop-1"] = len(c.buf)
    page_until(c, b"Sysop:", 12)
    c.pump(1.0)
    save(c, "setup-80", cols, marks)
    c.close()


if MODE == "setup":
    setup()
elif MODE == "config":
    run(CONFIG_SCENES, 80, "config-80")
    run(CONFIG_SCENES, 40, "config-40")
elif MODE == "camera":
    run(CAMERA_SCENES, 80, "camera-80")
elif MODE == "s3":
    run(S3_SCENES, 80, "s3-80")
