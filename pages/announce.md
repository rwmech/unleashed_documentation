<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Moved whole from setup.md's "announce" (guides, 2026-09-29, tty-ux's sysop guide spec). The Outside field is also cited from forward.md's "A name that follows your address". -->
# The directory listing

## announce

The directory listing: a short message the board sends every few minutes so it
appears on [the board list](/directory). **Off** as shipped, and the sysop's alone. It
sends the board's name, your name, the description, the port and how busy the
board is, and nothing about who is calling. `ANNOUNCE TEST` shows exactly what
it would send.

> Change the sysop password before you switch this on: the board will not list
> itself while the default password is still set. And [forward the
> port](/docs/forward) first, or callers will find a listing that does not answer.

<!-- Rob, 2026-10-06: the sweep for anything that sends a sysop the long way round. The warning above stays as it is: forwarding still has to happen, and this says who can do it. Gated on firmware 1.2.2. -->
::: from 1.2.2
From firmware 1.2.2 the board can do the forwarding part itself, and
`PORTMAP` tells you whether your router agreed, which is the thing to check
before the listing goes on. [How that
works](/docs/forward#or-let-the-board-ask-your-router).
:::

<!-- Site 1.3.10: from firmware 1.1.1 a closed board keeps announcing and sends "closed": true (PROTOCOL.md, Closed boards); 1.1.0 stops announcing while closed. -->
::: from 1.1.1
While the board is closed to callers, it stays on the list, marked
**Temporarily closed**, and its address is not offered as something to dial.
Open it again and the mark goes with the next announce.
:::

Every plugin page starts with the same four fields, which [the plugin
pages](/docs/config#the-plugin-pages) explain. Then:

<!-- The same list twice, so each is one list: firmware 1.1.0 relabels Port as Outside (copy-1.1.0 section 5). Edit both until a 1.1.0 release is on disk, then drop the "until" one. -->
::: until 1.1.0
- **Board**: The name the directory will show. It is the Board field on the
  board page, shown here, not a second copy.
- **Sysop**: Your name, as the directory shows it. Takes up to 40 characters.
- **About**: One line about the board. Takes up to 120 characters.
- **DNS name**: A name of your own that reaches the board, if you have one.
  Empty means the address the directory saw the message come from. Takes up to
  95 characters.
- **Port**: The port callers dial, if you forwarded a different one to the
  board's 6400. Takes 1 to 65535; as shipped, `6400`.
- **Directory**: Where to send it. Comma separated, up to four, so a board can
  be in several directories.
- **Every min**: Minutes between messages. Takes 1 to 1440; as shipped, `10`.
- **Push secs**: When somebody calls or leaves, the board tells the directory
  early, at most this often. 0 leaves only the timed message. Takes 0 to 3600;
  as shipped, `60`.
- **Activity**: Whether to include the board's calls and caller-minutes over
  the last 24 hours. Takes yes or no; as shipped, `no`.
- **Token**: Issued by the directory the first time, and kept so the listing
  survives a reflash. Leave it alone.
:::

::: from 1.1.0
- **Board**: The name the directory will show. It is the Board field on the
  board page, shown here, not a second copy.
- **Sysop**: Your name, as the directory shows it. Takes up to 40 characters.
- **About**: One line about the board. Takes up to 120 characters.
- **DNS name**: A name of your own that reaches the board, if you have one.
  Empty means the address the directory saw the message come from. Takes up to
  95 characters.
- **Outside**: The port callers dial from the internet, when your router
  forwards a different number to the board. Leave it empty if the router
  forwards the same number as **Port**, and the board sends that.
<!-- Firmware 1.2.2 (the firmware repository's ANNOUNCE.md on branch portmap-1.2.2, public_port): with port_map on and a mapping granted on a different outside port, an empty Outside publishes the granted port, because the listening port is then the one number that is certainly wrong. -->
::: from 1.2.2
  With [the board asking your router](/docs/forward#or-let-the-board-ask-your-router)
  switched on, and the router having given it a different outside number than
  it asked for, an empty **Outside** sends the number the router actually
  gave. So the listing follows the router without your doing anything.
:::
- **Directory**: Where to send it. Comma separated, up to four, so a board can
  be in several directories.
- **Every min**: Minutes between messages. Takes 1 to 1440; as shipped, `10`.
- **Push secs**: When somebody calls or leaves, the board tells the directory
  early, at most this often. 0 leaves only the timed message. Takes 0 to 3600;
  as shipped, `60`.
- **Activity**: Whether to include the board's calls and caller-minutes over
  the last 24 hours. Takes yes or no; as shipped, `no`.
- **Token**: Issued by the directory the first time, and kept so the listing
  survives a reflash. Leave it alone.
:::

::: from 1.0.1
From firmware 1.0.1 the page also takes the causes you support and what you
are into, as badges under the board's name: the codes on [the badges
page](/badges), separated by commas, in any case.
:::

The rest is on [the getting listed page](/how), and [the house
rules](/rules) are four lines.

Back to [Set up your BBS](/docs/setup).
