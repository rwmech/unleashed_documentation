<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Moved whole from setup.md's "First, become the sysop" (guides, 2026-09-29, tty-ux's sysop guide spec), anchor kept. The captures are from firmware 0.23.0: shot-setup-screen still tells the sysop to backspace over the stars, which firmware 1.0.0 made unnecessary (it still works). Recapture it, with the others, at 1.2.0; do not edit a capture by hand. -->
# First login: become the sysop

## First, become the sysop

A new board has one password, the sysop's, and it is `unleashed`. It only works
from your own network, and only until you change it. The install page says
[why](https://unleashedbbs.com/install#the-sysop-password). On your first call from your own network, the board
asks for it by itself, once you have signed up or logged in:

::: art
shot-setup-offer
:::

The right password makes you the sysop, and the board says so:

::: art
shot-setup-screen
:::

Then the staff passwords form opens by itself. Type a sysop password of your
own and press F1 to save it. The board will not take `unleashed` here.

::: art
shot-config-staff
:::

After that, a short tour of the settings, and then the sysop's prompt:

::: art
shot-newsysop-1
:::

<!-- Closed until opened (firmware 1.1.0): the firmware repo's CLAUDE.md, "A board is closed until its sysop opens it", a plan when this was written. Check the label against CONFIG board once it is built. -->
::: from 1.1.0
Until you open it, the board is closed to everybody else: other callers get
the busy message. When you have finished setting it up, open it on the board
page of `CONFIG` by turning **Stop taking calls** (**Closed** at 40 columns)
off.
:::

After that, on any call, you become the sysop by typing `BYE` and your password
at the prompt. The board moves you to its sysop node, and the prompt starts
with `[S]`. A wrong password is an ordinary log off, and three wrong from one
address within fifteen minutes locks that address out for fifteen minutes.

Every setting after that is on [the CONFIG page](/docs/config).

Back to [Set up your BBS](/docs/setup).
