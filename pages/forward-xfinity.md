<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
# Port forwarding on an Xfinity gateway

A rented Xfinity gateway, through the Xfinity app.

> This opens a door into your own network and you are responsible for what
> comes through it. Read [the warnings](/docs/forward) first if you have not.

<!-- Rob, 2026-10-06: "make sure documentations says something like 'Check to see if this works before you bother reserachiing your router'". The same paragraph on all five router pages, because a reader lands on one of them and never sees the other four. It sits under the warning box and above the first instruction: a pointer, not a shortcut past the warnings. Firmware 1.2.2's port_map is what the 1.2.2 half promises; PORTMAP TEST and its CONFIG network button were moved out of 1.2.2 on 2026-10-06 and are 1.2.3, so the test is its own nested gate and the 1.2.2 half still leaves a reader a complete route. Additive, never a swapped pair. This says what they tell you and never what they draw. -->
::: from 1.2.2
**Before you start,** it is worth knowing that from firmware 1.2.2 the board
can ask your router to set this up by itself. If your router answers, there is
nothing on this page for you to do. [Let the board ask your
router](/docs/forward#or-let-the-board-ask-your-router).

::: from 1.2.3
From firmware 1.2.3 it can also ask whether your router will, without making
any forward, so you can find out before you decide anything.
:::
:::

On a rented Xfinity gateway, port forwarding lives in the mobile app, not in
the gateway's own web page. Comcast states that customers with Xfinity Gateways
can only set up and adjust port forwarding using the Xfinity app.

## Steps in the app

1. Open the Xfinity app and sign in with a Primary, Manager or Member ID.
2. Select **WiFi**.
3. Select **View WiFi equipment**.
4. Select **Advanced Settings**.
5. Select **Port Forwarding**.
6. Select **Add Port Forward**, then **Continue**.
7. Pick the board from the device list. It must be connected, on IPv4, using
   DHCP.
8. Pick a preset, or select **Manual Setup** to enter ports and protocol.
9. Select **Next** to save.

For a board: choose Manual Setup, external and internal port both `6400`,
protocol TCP. Comcast's article confirms Manual Setup takes port numbers and
settings but does not print the field labels, so the exact wording on screen is
not quoted here.

## The web route, and the local page

Comcast's current documentation describes port forwarding in the app and
nowhere else.

The local Admin Tool at `http://10.0.0.1` still exists, but it has to be
switched on from the app first, and Comcast does not document port forwarding
in it. To switch it on: **WiFi > View WiFi equipment > Advanced Settings >
Admin Tool online access > Allow Admin Tool access > Save**. The username is
`admin`, and the password is the one you create when you switch it on.

## Reserving an address

A forward has to point at an address that does not move. The app binds the rule
to the device you picked rather than showing a reservation screen, and there is
no official Comcast article documenting a reserved-IP control in the app, so
treat any menu path you find for it as unverified. The route people commonly
use is the Admin Tool: **Connected Devices > Devices > Edit > Reserved IP**.
That comes from Comcast's forums, not its documentation.

One caveat from the official article: if the device uses MAC address
randomisation the rule will break, and a forward whose device has gone cannot
be edited, only deleted and recreated. Turn randomisation off for the board.

## Using your own router instead

Put the gateway in Bridge Mode: Admin Tool at `http://10.0.0.1` >
**Gateway > At a Glance > Enable** next to Bridge Mode. Routing stops and the
modem function stays. You lose the gateway's Wi-Fi, xFi network management,
Wi-Fi extenders and Xfinity CyberSecure, and only one device may connect by
Ethernet.
Your own router then does the forwarding.

## When it does not work

- **Xfinity CyberSecure**, previously Advanced Security. When it sees something
  aimed at a device with port forwarding, DMZ or UPnP ports open, it blocks all
  traffic from that device's open ports. Comcast recommends leaving it on and
  using Allow Access on the device; turning it off is the other way out. Worth
  checking first when the rule is correct and the traffic is still dropped.
- **Double NAT.** Your own router behind a gateway that is still routing gives
  two layers. The gateway's Bridge Mode is the fix. Double NAT and CGNAT on
  any router are explained on [the main port forwarding page](/docs/forward#two-things-that-will-stop-it-working).
- **IPv4 only.** The app's port forwarding is IPv4. Xfinity carries both, so a
  board reachable over IPv6 may still be unreachable over IPv4.

## Sources

- [xFi port forwarding](https://www.xfinity.com/support/articles/xfi-port-forwarding)
- [xFi advanced settings](https://www.xfinity.com/support/articles/xfi-advanced-settings)
- [Admin Tool access](https://www.xfinity.com/support/articles/admin-tool-access)
- [Enable or disable Bridge Mode](https://www.xfinity.com/support/articles/wireless-gateway-enable-disable-bridge-mode)
- [Using xFi Advanced Security](https://www.xfinity.com/support/articles/using-xfinity-xfi-advanced-security)
- [About IPv6](https://www.xfinity.com/support/articles/about-ipv6)
