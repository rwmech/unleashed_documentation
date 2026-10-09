"""
===========================================================================
 µnleashed BBS guides
===========================================================================
File:         shots/capture/cfg.py
Purpose:      The settings file a capture board runs on: the firmware's own
              shipped data/system.cfg.example, so every screen shows the
              values a new board ships with, plus a sysop password, the
              board open, and the card plugins given something to show.

Usage:        cfg.py <firmware checkout> <out file> <backup port>

Copyright 2026 - Robert Mech
License:      GNU General Public License v3 or later
SPDX-License-Identifier: GPL-3.0-or-later
===========================================================================
"""
import re
import sys

FW, OUT, BACKUP = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(FW + "/data/system.cfg.example", encoding="utf-8").read()

TOP = {"sysop_password": "docshots", "backup_port": BACKUP, "closed": "no"}
SECTIONS = {
    "plugin:files": {"enabled": "yes", "area1": "pub/c64 | C64 Downloads",
                     "area2": "pub/text | Text Files"},
    "plugin:forums": {"enabled": "yes", "topic1": "general | General | Anything at all",
                      "topic2": "news | Board News | What the sysop is up to | all | sysop "
                                "| users | sysop"},
    "plugin:info": {"page0": "House rules | all"},
    "plugin:announce": {"name": "My Board", "owner": "Sparks",
                        "description": "A board in a box on the shelf"},
    "plugin:link": {"enabled": "yes"},
    "plugin:camera": {"enabled": "yes"},
}


def set_key(block, key, value):
    """block with key set: its line replaced (commented out or not), or
    added at the end."""
    pat = re.compile(rf"(?m)^[#;]?[ \t]*{re.escape(key)}[ \t]*=.*$")
    if pat.search(block):
        return pat.sub(f"{key} = {value}", block, count=1)
    return block.rstrip("\n") + f"\n{key} = {value}\n"


# Keys above the first section.
first = re.search(r"(?m)^\[", text)
head, rest = (text[:first.start()], text[first.start():]) if first else (text, "")
for k, v in TOP.items():
    head = set_key(head, k, v)
parts = re.split(r"(?m)^(?=\[)", rest)
seen = set()
for i, part in enumerate(parts):
    m = re.match(r"\[([^\]]+)\]", part)
    if m and m.group(1) in SECTIONS:
        seen.add(m.group(1))
        for k, v in SECTIONS[m.group(1)].items():
            part = set_key(part, k, v)
        parts[i] = part if part.endswith("\n\n") else part.rstrip("\n") + "\n\n"
extra = "".join(f"[{s}]\n" + "".join(f"{k} = {v}\n" for k, v in kv.items()) + "\n"
                for s, kv in SECTIONS.items() if s not in seen)
open(OUT, "w", encoding="utf-8").write(head.rstrip("\n") + "\n\n" + "".join(parts) + extra)
