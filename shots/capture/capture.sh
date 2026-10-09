#!/bin/sh
# ===========================================================================
#  µnleashed BBS guides
# ===========================================================================
# File:         shots/capture/capture.sh
# Purpose:      Capture every screen the guides show, from one firmware
#               checkout, in one command, and write shots/*.json stamped with
#               that firmware's version. Run it for each firmware release.
#
# Usage (in WSL or Linux, from this repository):
#   sh shots/capture/capture.sh <firmware checkout>
#
# The checkout is a worktree of its own, never somebody's working tree:
#   git -C <firmware repo> worktree add --detach <scratch>/fw origin/main
#
# It builds the host boards (host/bbs_host, bbs_host_fncam and, for the
# S3's SSH screens, bbs_host_ws43b), stands each one up on 127.0.0.1 on the
# docshots tag's port with a settings file close to a fresh install's, drives
# a session through the screens (capture.py), stops the board, and turns
# the sessions into shots/*.json (tojson.py). Only this tag's boards are
# ever killed, and nothing talks to anything but 127.0.0.1.
#
# Copyright 2026 - Robert Mech
# License:      GNU General Public License v3 or later
# SPDX-License-Identifier: GPL-3.0-or-later
# ===========================================================================
set -e
FW=$(cd "$1" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
SHOTS=$(cd "$HERE/.." && pwd)
VER=$(sed -n 's/^#define BBS_VERSION *"\([^"]*\)".*/\1/p' "$FW/src/config.h")
REV=${REV:-$(git -C "$FW" rev-parse --short HEAD 2>/dev/null || echo unknown)}
TOP=/tmp/bbs-docshots
CAP=$TOP/cap
PORT=$((6500 + $(printf '%s' docshots | cksum | cut -d' ' -f1) % 400))
export BBS_LINK_PORT=$((PORT + 3000))
export BBS_LINK_PEER_PORT=$((PORT + 3001))
export BBS_HOST_SSID=HomeNet

echo "capturing firmware $VER ($REV) on port $PORT"
(cd "$FW/host" && make -s bbs_host bbs_host_fncam bbs_host_ws43b)
rm -rf "$CAP"
mkdir -p "$CAP"

# A board of one kind, with one settings file, driven through one mode.
board() {
    BIN=$1; MODE=$2; FRESH=$3
    DATA=$TOP/data-$MODE
    CARD=$TOP/card-$MODE
    pkill -f "$BIN $DATA" 2>/dev/null && sleep 0.3 || true
    rm -rf "$DATA" "$CARD"
    mkdir -p "$DATA/user" "$CARD/pub/c64" "$CARD/pub/text" "$CARD/forums"
    cp -r "$FW/data/." "$DATA/"
    rm -f "$DATA/system.cfg" "$DATA/users.txt" "$DATA/calls.log"
    rm -rf "$DATA/logs"
    if [ "$FRESH" = fresh ]; then
        # A board straight off the installer: no staff password lines, so
        # the published default applies and the setup is offered.
        printf 'tz = UTC0\nbackup_port = %s\n' $((PORT + 1000)) > "$DATA/user/system.cfg"
    else
        # The firmware's shipped settings file, so the screens show what a
        # new board ships with, plus what cfg.py adds.
        python3 "$HERE/cfg.py" "$FW" "$DATA/user/system.cfg" $((PORT + 1000))
    fi
    (cd "$FW/host" && BBS_SD_DIR="$CARD" ./"$BIN" "$DATA" "$PORT" > "$TOP/$MODE.log" 2>&1 &)
    sleep 1.5
    python3 -u "$HERE/capture.py" "$FW" "$CAP" "$PORT" "$MODE" || true
    pkill -f "$BIN $DATA" 2>/dev/null || true
    sleep 0.3
}

board bbs_host setup fresh
board bbs_host config normal
board bbs_host_fncam camera normal
board bbs_host_ws43b s3 normal

# Every capture comes from this run, so the old set goes first: a screen
# the guides stopped using, or one that did not come out, does not linger
# under an older firmware's stamp.
rm -f "$SHOTS"/*.json
python3 "$HERE/tojson.py" "$CAP" "$SHOTS" "$VER" "$REV"
echo "done: shots/*.json from firmware $VER ($REV)"
