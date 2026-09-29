<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Site 1.3.0 (Rob, marketing round 3): "Go public" became "Let others in" in the menu, and this title says what the reader gets. The warning stays first, before any instructions, and the router instructions below keep their technical words, each explained where it first appears. -->
# Let people outside your home join

[[Port forwarding]] is the step that turns a board on your desk into a board
anyone can join from anywhere, where the BBS world says "call". It is one
setting on your router, and it is the setting with the most consequences, so
this page is blunt about what it does before it tells you how.

> **Read this first. You are opening a door in your own network, and you are
> the only person responsible for what comes through it.** Nobody here can see
> your network, your router, or what else is on it. If you do not understand
> what a port is, stop and read until you do. If the network belongs to your
> employer, your landlord, your university or your parents, ask them first.

## What you are doing

Your router blocks unsolicited traffic from the internet by default. That
default is the single largest thing protecting the devices in your house:
printers, cameras, NAS boxes, a television, anything that was built by
somebody in a hurry and has not been updated since.

A port forward makes one exception to it. You are telling the router: traffic
arriving on this port is expected, send it to this machine. Done correctly,
exactly one program on exactly one device becomes reachable. Done carelessly,
you can expose something you never meant to.

## The specific risks

> **Telnet is plain text.** This is a BBS, and the protocol has no encryption.
> Every password typed by every visitor crosses the open internet in the
> clear, and anybody positioned between a visitor and your board can read all
> of it. That is a property of the protocol, not a bug in this software, and
> it was true of every board in 1985 too. Tell the people who join, and never
> reuse a password on a telnet board. A board on an ESP32-S3 also takes
> [SSH](/docs/terminals#connect-with-ssh), which is encrypted, on the same port
> and on its own, 6422 as shipped: forward that one too if you want visitors
> from outside to use it with SyncTERM.

- **You will be scanned within minutes.** Every address on the internet is
  swept continuously by automated scanners. This is normal and not personal,
  but it means an open port is found almost immediately.
- **Your address becomes public.** A listing on a directory publishes it
  deliberately, and that address is roughly where you live. If that matters to
  you, host the board somewhere else.
- **A bug in this software becomes a bug on the internet.** It is written
  carefully and tested, and it is still a program on a chip written by
  hobbyists. Forwarding a port means trusting it with strangers.
- **Forward one port, not a range, and never DMZ.** A DMZ setting forwards
  everything to one device. Do not use it for this.
- **Your ISP may not allow it.** Plenty of residential terms of service
  prohibit running a server. That is between you and them.

## Two things that will stop it working

Before blaming the router, check these. Between them they account for most
failures, and the second one cannot be fixed by any setting at all.

- **Double NAT.** If your router's WAN address is itself private, starting
  `192.168.`, `10.` or `172.16`-`172.31`, there is a second router upstream,
  usually an ISP box. The forward has to exist on the outermost device, or
  the ISP box has to be put in bridge mode.
- **CGNAT.** If your WAN address falls in `100.64.0.0` to `100.127.255.255`,
  or does not match what an external "what is my IP" service reports,
  your ISP is sharing one public address among many customers. No router
  setting will ever make an inbound port work. Common on mobile and some
  fibre plans. Your options are asking the ISP for a public address, IPv6, or
  an outbound tunnel.

Also worth knowing: these rules are IPv4 only on effectively all consumer
routers. IPv6 is handled separately, usually as a firewall rule rather than a
forward, because there is no address translation to undo.

## The same port outside and in

A forward has two port numbers. The outside one, which routers also call the
external port, is the one visitors connect to from the internet. The inside one, the
internal port, is where the router sends them on the board. The simplest
forward uses the same number for both, 6400 outside to 6400 on the board, and
every router page below does it that way.

Some routers can do nothing else. They have one port box, not two, and send a
call to the same number it arrived on. eero is one: [its page](/docs/forward-mesh)
says so. On a router like that, the number callers dial and the number the
board listens on have to be the same.

## One board per port

Your home has one address on the internet, and one outside port on it can go
to one device and no more. So a second board behind the same router needs an
outside port of its own: 6400 for the first board, say, and 6401 for the
second. One board per port.

::: from 1.1.0
The way that works on every router is to give each board its own port to
listen on, so every forward is the same number outside and in. From firmware
1.1.0 that is **Port** on [the network page of `CONFIG`](/docs/config#network),
used from the next restart.

So set the second board's **Port** to 6401, restart it, and forward 6401 to
6401 at that board's address. Callers on your own network dial it on 6401 as
well.

A router that can send one outside number to a different number inside gives
you the other way: leave both boards on 6400 and forward 6401 outside to 6400
on the second board. Then the second board has to tell the directory which
number callers dial, which is **Outside** on [the announce page of
`CONFIG`](/docs/announce): the port callers dial from the internet.
:::

::: until 1.1.0
Every board listens on 6400, so the second board's forward has to change the
number on the way in: 6401 outside, to 6400 on that board. That needs a
router with separate outside and inside port boxes. Then the second board has
to tell the directory which number callers dial, which is the **Port** setting
on the announce page of `CONFIG`: set it to 6401.
:::

This directory lists one board per internet address by itself. A second board
from the same address waits for the person who runs the directory to let it
through.

<!-- New for the guides' setup hub (2026-09-29, tty-ux's sysop guide spec). The directory learning the address from the announce is the listing's X-Seen-Address (PROTOCOL.md); DNS name and Outside are announce's own fields, on /docs/announce. The router and eero notes are forward-netgear.md's and forward-mesh.md's. -->
## A name that follows your address

Unless you pay your internet provider for a fixed address, the one your home
has on the internet changes now and then. Anybody who wrote down the old
numbers dials nothing.

- **The directory keeps up by itself.** A listed board tells the directory
  it is still there every few minutes, and the directory lists it at the
  address it hears from, so a listing follows a new address with no help.
- **For callers who dial you directly,** give them a name instead of the
  numbers: dynamic DNS. A dynamic DNS service gives you a name, and a small
  program keeps it pointed at your current address. Many routers have one
  built in, under a name like Dynamic DNS or DDNS; on eero it needs eero
  Plus, as [its page](/docs/forward-mesh) says.
- **Put the name in the listing** too: **DNS name** on [the directory listing's
  page](/docs/announce) makes the directory show your name rather than the
  numbers. When your router forwards a different number outside than the
  board's **Port**, **Outside** on the same page is the number callers dial.

## Pick your router

- [NETGEAR](/docs/forward-netgear) - Nighthawk and R-series, routerlogin.net
- [TP-Link](/docs/forward-tplink) - Archer series and Deco mesh
- [ASUS](/docs/forward-asus) - RT-AX and RT-AC on ASUSWRT
- [Xfinity / Comcast](/docs/forward-xfinity) - a rented Xfinity gateway, through the app
- [eero and Google Nest Wifi](/docs/forward-mesh) - the app-only mesh systems

Menu names move between firmware versions, and vendors rename things without
warning. Where a vendor does not document something, these pages say so rather
than guessing, because a confidently wrong menu path wastes more of your time
than an honest gap.

## A safer way to try it first

You do not have to open anything to run a board. On your own network it works
immediately, and people on the same Wi-Fi can connect by address or by
`unleashed.local` with [a free app for joining](/docs/terminals). To let people
outside reach it without opening a port, use a VPN into your own network or a
tunnel from a machine you rent. Both work, and neither puts your address on a
scanner's list.

Forward the port when you have decided you want a public board, not to find
out whether the software works.
