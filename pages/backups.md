<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Moved whole from setup.md's "backup" (guides, 2026-09-29, tty-ux's sysop guide spec), anchor kept; the pointer to the card's nightly backups is new. -->
# Backups

::: applies
Firmware 1.2.0
:::

## backup

The backup window: a way to copy the board's settings, accounts and screens off
it as one zip file, and to put a copy back, from a computer on your network.

- **Port** (`backup_port`): The web port the window opens on. It cannot be
  the port callers use, which is 6400 as shipped. Takes 1 to 65535; as
  shipped, `8080`.
- **Open for** (`backup_window_minutes`): How long one press of the button
  keeps the window open. Takes 1 to 60 minutes; as shipped, `5`.
- **Button** (`backup_button_gpio`): The pin of the button that opens it. 0 is
  the BOOT button on a dev board. Takes 0 to 39; as shipped, `0`.

To use it, log in as the sysop, then press BOOT on the board. While the window
is open, from a computer on the same network:

```
curl -o backup.zip http://<board>:8080/backup.zip
curl -T backup.zip http://<board>:8080/restore
```

On Windows, type `curl.exe` rather than `curl`. The first line downloads a
copy, with no question asked. The second sends one back: the board shows what
arrived on the sysop's screen and asks `Accept upload (Y/N)?`, and nothing
changes unless you answer Y within two minutes.

> A backup holds the staff passwords only as three asterisks and account passwords only as
> salted hashes, but it holds the **Wi-Fi password as typed**. That is why the
> board only hands one to an address on your own network. Keep backups
> somewhere private.

The window closes when its minutes are up or when the sysop logs off.

## Backups on the card

A board with an SD card can also back itself up onto the card every night:
the **Nightly** setting, on [the SD card's settings](/docs/sdcard#settings).

Back to [Set up your BBS](/docs/setup).
