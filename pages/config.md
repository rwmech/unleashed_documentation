<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Moved whole from setup.md (guides, 2026-09-29, tty-ux's sysop guide spec): How CONFIG works, board, limits, accounts, staff, wifi and network, the plugin pages, serial and example. Anchors kept. The backup page's settings moved to /docs/backups, the SSH port row to /docs/ssh, and each plugin's settings to its own guide. -->
# Every setting: CONFIG

::: applies
Firmware 1.2.0
:::

Every setting on a µnleashed board can be changed from the board itself, while
you are logged in as the [[sysop]], the host, with one command: `CONFIG`. Nothing needs a
laptop, a text editor or a reflash.

## How CONFIG works

Type `CONFIG` on its own and the board lists its settings pages: six of its own,
then one for each plugin, which is a feature the board can switch on or off.

::: art
shot-config-list
:::

Type `CONFIG` and a page's name, such as `CONFIG board`, and that page opens as
a form.

::: art
shot-config-board
:::

- **Tab or the arrow keys** move between fields, as the bottom line says.
- **F1 saves.** Only the fields you changed are written, and the rest of the
  board's settings file is left exactly as it was, comments included.
- **ESC leaves** without saving.
- **Saved means live.** The board reloads the settings at once. The exceptions
  are the network page (called wifi before firmware 1.1.0), the hostname and
  the NTP server, which are used from the next restart.
- **A value outside what a field accepts is refused** before anything is
  written, so a typo cannot take a page down.
- **One sysop at a time.** CONFIG is the sysop's alone: co-sysops do not get it,
  because it can change the staff passwords.

These screens were captured from the board's own software, version 0.23.0,
running on a test machine: the setup at 80 columns and the CONFIG pages at 48.
On a wider terminal the lists are wider, and since firmware 1.1.0 a terminal
of 80 columns or more gets longer form labels, such as **Onboard LED GPIO**
where 40 columns say **Board LED**.

## board

The board's name and clock, and where callers land.

- **Board** (`board_name`): The board's name. The welcome screen tells callers
  who they are connecting to, and the directory lists the board under it. Empty
  means the software's own name. Takes up to 40 characters; as shipped, `My
  Board`.
- **Hostname** (`hostname`): The board's name on your network, for the router's
  list of devices and for `name.local` on computers that look those up. Used
  from the next restart. Takes a to z, 0 to 9 and `-`, up to 31 characters; as
  shipped, `unleashed`.
- **Timezone** (`tz`): The local time, as a POSIX time zone string. The number
  is hours **west** of UTC, so US zones are positive. `UTC0` is UTC;
  `EST5EDT,M3.2.0,M11.1.0` is US Eastern; `GMT0BST,M3.5.0/1,M10.5.0` is the UK;
  `CET-1CEST,M3.5.0,M10.5.0/3` is central Europe. Takes up to 40 characters; as
  shipped, `UTC0`.
- **NTP** (`ntp_server`): Where the board gets the time from. Used from the
  next restart. Takes up to 40 characters; as shipped, `pool.ntp.org`.
- **Idle min** (`idle_minutes`): How long a caller can sit at the prompt doing
  nothing before the board hangs up. It warns a minute before. Takes 1 to 240
  minutes; as shipped, `20`.
- **LED gpio** (`activity_led_gpio`): The pin of an LED that blinks with
  network traffic. 2 is the blue LED on the common DOIT-style dev boards. Takes
  0 to 39; as shipped, `2`.
- **Land on** (`landing`): Where a caller goes after logging in, unless their
  own account says otherwise. Takes `main`, `chat` or `forums`; as shipped,
  `main`.

## limits

How long callers can stay.

- **Per call** (`call_minutes`): The longest one call can last. Takes 1 to 1440
  minutes; as shipped, `60`.
- **Per day** (`day_minutes`): The most minutes one account can spend on the
  board in a day, over all its calls. Takes 1 to 1440 minutes; as shipped,
  `480`.
- **WHO min** (`who_refresh_min`): The fastest a caller can make the `WHO` and
  `DASH` screens refresh themselves, in seconds. Takes 1 to 60; as shipped,
  `1`.
- **WHO max** (`who_refresh_max`): The slowest, in seconds. Takes 1 to 60; as
  shipped, `30`.
- **Accounts** (`max_users`): The most accounts the board will hold. When it is
  full, nobody new can sign up. Takes 1 to 250; as shipped, `100`.

Staff can be spared the limits: the `NOLIMITS` permission, which every staff
level has as shipped, means no idle hang-up and no call or daily limit.

## accounts

Who can get in.

- **Sign-ups** (`self_register`): Whether somebody with a handle the board has
  not seen is offered **[R]egister**. With `no`, only staff can create
  accounts, from the `USERS` manager. Takes yes or no; as shipped, `yes`.
- **Guests** (`guest`): Whether that somebody is also offered **[G]uest**: a
  call with no account, where nothing is saved and the handle is marked `*` in
  every list. Takes yes or no; as shipped, `yes`.
- **Guest mn** (`guest_minutes`): How long a guest call can last. Guests have
  no daily limit. Takes 1 to 240 minutes; as shipped, `15`.

## backup

The backup window's page, and how to use it, are on [backups](/docs/backups).

## staff

The three staff passwords. A caller becomes staff by typing `BYE` and one of
these at the prompt.

- **Sysop** (`sysop_password`): Moves you to the sysop node, with every
  permission, CONFIG included. Takes up to 32 characters, case-sensitive; as
  shipped, `unleashed` until you change it.
- **Co-sysop 1** (`cosysop1_password`): Grants co-sysop 1 on the line you are
  already on, with the permissions described below. Takes up to 32
  characters; empty as shipped.
- **Co-sysop 2** (`cosysop2_password`): The same for co-sysop 2, with fewer
  permissions. Takes up to 32 characters; empty as shipped.

Passwords on this page:

- A password already set shows as `********`, and is only written when you type
  a new one.
- An empty password switches that level off.
- Use passwords you use nowhere else. Calls over telnet are not encrypted, which
  [the privacy page](/docs/privacy) explains in plain terms; on an ESP32-S3
  board, [calls over SSH](/docs/terminals#connect-with-ssh) are.

What a co-sysop may do is a table in the board's settings file, not a CONFIG
page. As shipped, both co-sysop levels may list who is on with their addresses,
broadcast, add or take away a caller's time, see the ban list, see the
dashboard, and skip the time limits. Co-sysop 1 may also kick and watch callers,
hide from the lists and manage accounts; only the sysop may lift a ban. To
change that table, edit the settings file inside a backup and send it back
through [the backup window](/docs/backups).

<!-- Firmware 1.1.0 renames this page "network" (CONFIG wifi still opens it) and adds Port. The two gates swap the account on the day a 1.1.0 release is on disk. Words for Port from the firmware repo's internal/copy-1.1.0-2026-09-23.md section 5. -->
::: until 1.1.0
## wifi

The network the board joins.

- **Network** (`wifi_ssid`): The name of the Wi-Fi network. Takes up to 32
  characters; set to what you chose when installing.
- **Password** (`wifi_password`): Its password. Takes 8 to 64 characters, or
  empty for an open network.
:::

::: from 1.1.0
## network

The network the board joins, and the port callers dial. `CONFIG network` opens
it, and so does `CONFIG wifi`, its name before firmware 1.1.0.

- **Network** (`wifi_ssid`): The name of the Wi-Fi network. Takes up to 32
  characters; set to what you chose when installing.
- **Password** (`wifi_password`): Its password. Takes 8 to 64 characters, or
  empty for an open network.
- **Port** (`port`): The port callers dial. Used from the next restart. It
  cannot be the backup window's port. Takes 1 to 65535; as shipped, `6400`.
  If callers reach the board from the internet, the forward on your router has
  to point at the new number too. When you would change it is under [one
  board per port](/docs/forward#one-board-per-port).
- **CGNAT/Tailscale LAN** (`cgnat_local`), **CGNAT** at 40 columns: Whether
  addresses in 100.64.0.0/10, the carrier-grade NAT range Tailscale also
  uses, count as the board's own network. From firmware 1.1.1. It trusts
  everybody behind the same carrier NAT, not only your own devices, which is
  why it is off as shipped.
- **SSH port (SyncTERM)** (`ssh_port`), ESP32-S3 boards only: on [the SSH
  page](/docs/ssh#the-ssh-port).
:::

A change here is used from the **next restart**, never straight away, because
changing the network under your own call would drop you, and a typo would leave
nobody on the board to put it right. A network the board cannot join within a
minute of the restart is given up for the last one that worked. If the board
still cannot reach its network, the fix is the cable: [the install page](https://unleashedbbs.com/install) changes the Wi-Fi from your
browser.

## The plugin pages

Every plugin's page starts with the same four fields:

| Field | What it does |
|---|---|
| **Enabled** | yes or no. A plugin that is off costs nothing: no commands, no memory. |
| **Read** | Who may use it to look. |
| **Write** | Who may use it to change something. |
| **Admin** | Who may configure it. |

The levels, from widest to narrowest: `all` (anybody, guests too), `users`
(anybody with an account), `staff` (any staff level), `co2`, `co1` and `sysop`.
Each one lets in that level and every level after it.

Each plugin's own settings are on its guide: [chat and mail](/docs/chat),
[forums](/docs/forums), [information pages](/docs/info), [files and the SD
card](/docs/sdcard#settings), [the directory listing](/docs/announce) and
[lights](/docs/lights).

## Other plugins

### serial and example

Both are **off** as shipped. The serial bridge shares a device wired to the
board's second serial port, where one person types and anybody else may watch,
and its page sets the pins, the speed and the format. The example plugin does
nothing useful; it is the template for somebody writing a plugin of their own.

Back to [Set up your BBS](/docs/setup).
