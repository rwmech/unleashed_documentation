"""
===========================================================================
 µnleashed BBS guides
===========================================================================
File:         shots/capture/tojson.py
Purpose:      Turn the sessions capture.py saved into one JSON file per
              screen in shots/, stamped with the firmware they came from.
              The directory draws each as the site's art (server.py,
              shot_svg): the characters on a grid, in the terminal's colours.

Usage:        tojson.py <capture dir> <shots dir> <version> [revision]

Each file holds the screen as the board drew it: the rows of text, and for
every cell one character of attribute, '0'-'f' for the colour (0-7, plus 8
when bold) and 'g'-'v' for the same colours in reverse video. Blank rows
above and below are dropped, and so are columns right of the widest row.
Alongside: "version" (the firmware's BBS_VERSION), "caption" (under the
glass, with the version) and "alt" (what the screen says, for a screen
reader, with the version). A 40 column capture is saved as <name>-40.

Copyright 2026 - Robert Mech
License:      GNU General Public License v3 or later
SPDX-License-Identifier: GPL-3.0-or-later
===========================================================================
"""
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import vt  # noqa: E402

SRC = pathlib.Path(sys.argv[1])
DST = pathlib.Path(sys.argv[2])
VER = sys.argv[3]
REV = sys.argv[4] if len(sys.argv) > 4 else ""

# What was typed to reach each screen, for its caption.
CAPTIONS = {
    "setup-offer": "after signing up, from the board's own network",
    "setup-screen": "the default password, typed at that question",
    "setup-staff": "then the staff passwords form, by itself",
    "newsysop-1": "saved: the tour, page 1",
    "config-list": "typed: CONFIG",
    "config-board": "typed: CONFIG board",
    "config-limits": "typed: CONFIG limits",
    "config-accounts": "typed: CONFIG accounts",
    "config-backup": "typed: CONFIG backup",
    "config-staff": "typed: CONFIG staff",
    "config-network": "typed: CONFIG network",
    "config-chat": "typed: CONFIG chat",
    "config-forums": "typed: CONFIG forums",
    "config-info": "typed: CONFIG info",
    "config-announce": "typed: CONFIG announce",
    "config-sd": "typed: CONFIG sd",
    "config-lights": "typed: CONFIG lights",
    "config-files": "typed: CONFIG files",
    "config-area": "typed: CONFIG files, then Enter on Area 1",
    "chat-room": "typed: CHAT",
    "chat-line": "in the room, a line typed and sent",
    "forums-list": "typed: FORUMS",
    "info-list": "typed: INFO",
    "sats-list": "typed: SATS",
    "config-camera": "typed: CONFIG camera, on a camera board",
    "config-photos": "typed: CONFIG photos, on a camera board",
    "snapshot": "typed: SNAPSHOT, on a camera board",
    "s3-config-network": "typed: CONFIG network, on an ESP32-S3 board",
    "s3-config-list": "typed: CONFIG, on an ESP32-S3 board",
    "s3-hardware": "typed: HARDWARE, on an ESP32-S3 board",
}

DST.mkdir(parents=True, exist_ok=True)
today = datetime.date.today().isoformat()
written = []
for meta_file in sorted(SRC.glob("*.json")):
    tag = meta_file.stem                           # config-80, setup-80, ...
    meta = json.loads(meta_file.read_text())
    data = (SRC / (tag + ".bin")).read_bytes()
    cols = meta["cols"]
    for name, mark in meta["marks"].items():
        if mark is None or mark < 0:
            print("SKIPPED", tag, name, "(no mark)")
            continue
        s = vt.Screen(cols, 24).feed(data[:mark])
        rows = s.text()
        used = [i for i, r in enumerate(rows) if r.strip()]
        if not used:
            print("EMPTY", tag, name)
            continue
        top, bottom = used[0], used[-1]
        width = max(len(rows[i].rstrip()) for i in range(top, bottom + 1))
        out_rows, out_attr = [], []
        for y in range(top, bottom + 1):
            text, attr = "", ""
            for x in range(width):
                ch, fg, bold, rev = s.grid[y][x]
                code = fg + (8 if bold else 0)
                text += ch
                attr += ("0123456789abcdef"[code] if not rev else "ghijklmnopqrstuv"[code])
            out_rows.append(text)
            out_attr.append(attr)
        out = name if cols >= 80 else name + "-" + str(cols)
        caption = CAPTIONS.get(name, name) + ", firmware " + VER
        said = re.sub(r"\s+", " ", " ".join(r.strip() for r in out_rows)).strip()
        if len(said) > 360:
            said = said[:357].rsplit(" ", 1)[0] + "..."
        doc = {
            "source": f"unleashed BBS {VER}" + (f" ({REV})" if REV else "")
                      + f", host build, ANSI at {cols} columns, captured {today}",
            "version": VER,
            "caption": caption,
            "alt": f"{CAPTIONS.get(name, name)}, at {cols} columns, firmware {VER}: {said}",
            "cols": width,
            "rows": out_rows,
            "attrs": out_attr,
        }
        with open(DST / (out + ".json"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        written.append(out)
        print(f"{out}: {width} x {len(out_rows)}")
print(len(written), "screens from firmware", VER)
