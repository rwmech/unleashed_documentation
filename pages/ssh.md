<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- The sysop's half of SSH (guides, 2026-09-29, tty-ux's sysop guide spec). Facts from the firmware's CLAUDE.md, 1.1.2 part 3: SSH on every ESP32-S3 profile, on the callers' port for clients that speak first and on ssh_port (6422, 0 off) where the board speaks first; host keys made at first start, their fingerprints OpenSSH-style in SYS and HARDWARE for staff. The ssh_port row is moved whole from setup.md's network page. The caller's half is terminals.md's "Connect with SSH". -->
# SSH on your board

Every ESP32-S3 board takes [[SSH]] beside telnet, from firmware 1.1.2: callers
whose app can encrypt get an encrypted call, and telnet stays open for the
machines that cannot. There is nothing to switch on. How a caller connects is
on [connect with SSH](/docs/terminals#connect-with-ssh).

## The SSH port

SSH answers on the port callers already dial. It also has a port of its own,
for SyncTERM 1.9 and older, which wait for the board to speak first:

- **SSH port (SyncTERM)** (`ssh_port`), **SSH port** at 40 columns, ESP32-S3
  boards only, from firmware 1.1.2: SSH's own port, where the board speaks
  first, for SyncTERM 1.9 and older. Used from the next restart. `0` turns it
  off, and SSH still works on **Port**. As shipped, `6422`. It is on the
  network page of [CONFIG](/docs/config#network).

::: art
shot-s3-config-network
:::

## The board's keys

The board makes its own host keys the first time it starts. An SSH app asks
you to trust a board's key on the first call; to check it is really your
board, compare the fingerprint the app shows with the one `SYS` shows the
sysop. The keys are not in a backup.

`HARDWARE` shows the sysop the same fingerprints, at its foot:

::: art
shot-s3-hardware
:::

Back to [Set up your BBS](/docs/setup).
