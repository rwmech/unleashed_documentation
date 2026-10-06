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

<!-- Rob, 2026-10-06: "make sure documentations says something like 'Check to see if this works before you bother reserachiing your router'". It sits under the warning and not over it: the page's rule is warning before instructions, and this is a pointer rather than a shortcut past them.

Two gates, not one, and the split is the point. Port mapping itself (port_map, PORTMAP) ships in firmware 1.2.2; PORTMAP TEST and the CONFIG network button that runs it were moved OUT of 1.2.2 by Rob on 2026-10-06 and are 1.2.3. So the 1.2.2 half must leave a complete route behind rather than a dangling pointer: switching the setting on and reading PORTMAP answers the same three questions, and on a connection that is not on the internet it answers them without exposing anything, because a forward made on a router that is not on the internet reaches nobody. The 1.2.3 half adds only the part that is genuinely new, asking without making a forward at all. Additive, never a swapped pair, so nothing here can leave a reader on 1.2.2 with "see above".

The button is named at its 80 column label, "Run port map test", and only that one: no short form for a 40 column form exists in any repository yet, and /docs/config names the port_map setting at both widths but the button at neither. When the firmware settles the 40 column label, add it to /docs/config beside the setting's and then say so here. -->
::: from 1.2.2
**Try this before you look anything up.** From firmware 1.2.2 the board can
ask your router to set the forward up itself, which on a router that answers
means there is no menu on this page for you to find.

It is worth a keypress before an evening of research. If your router answers,
you can [let the board do the whole
thing](/docs/forward#or-let-the-board-ask-your-router) and there is nothing
on this page to look up, though everything the next two sections say about
the risks still holds, and that section says so itself. If the board comes
back saying your address is not on the internet, then [no router setting of
any kind would ever have worked](/docs/forward#two-things-that-will-stop-it-working),
and it is much better to find that out now. If no router answers at all, read
on: forwarding the port by hand works on any router.

::: from 1.2.3
From firmware 1.2.3 you need not even switch it on to find out. The board can
put the question to your router without making any forward: `CONFIG network`
has a **Run port map test** button beside the setting, and the test opens
nothing.
:::
:::

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

<!-- Firmware 1.2.2's port_map maps both ports (src/core/portmap.h: the telnet port always, the SSH port too on a board that has one bound, and never the backup window's), so the warning above is incomplete from 1.2.2 rather than wrong. Gated. -->
::: from 1.2.2
Letting the board do the asking covers both: it asks for the port callers
dial and, on a board with an SSH port of its own, for that one as well. It
never asks for the backup window's port, which is meant to stay on your own
network.
:::

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

<!-- Firmware 1.2.2's port_map, from the firmware repository (branch portmap-1.2.2): src/core/portmap.h for the three protocols, the probe order, the 7200 s lease renewed at half, the permanent-mapping fallback on IGD error 725 and the private-outside-address reading; COMMANDS.md for the CONFIG row and PORTMAP; data/system.cfg.example for the key. Gated, so none of it appears until a release carrying it is on disk. The lease numbers are RFC 6886's own RECOMMENDED values, and the external-interface rule is quoted from its Security Considerations. The "no password" position is UPnP IGD's design, not a defect: the UPnP Device Architecture assumes a trusted home network and the IGD service has no authentication. Rob, 2026-10-06: "if a user uses this feature we need to fully disclose that its working and how it works." The order here is the page's own rule, warning before instructions. -->
::: from 1.2.2
## Or let the board ask your router

Most routers will set a forward up for a device that asks them from inside
the house, and from firmware 1.2.2 the board can do the asking. It is the
same mechanism a games console or a video call uses when it works without
anybody opening a menu.

> **This opens the same door.** Everything above is still true: the port is
> open to the whole internet, you will be scanned, your address becomes
> public, and telnet carries passwords in the clear. The only thing that
> changes is who types the setting in.

<!-- Firmware 1.2.3's PORTMAP TEST and its CONFIG network button, moved out of 1.2.2 by Rob on 2026-10-06. The whole section is the test, so the whole section is gated: on 1.2.2 a reader goes straight from the warning to "Switching it on", and "It will tell you when your ISP is in the way" below still answers the CGNAT question for them from PORTMAP. Nothing outside this gate may link this anchor. -->
::: from 1.2.3
### Finding out without switching anything on

The board can put the question to your router without making a forward and
without opening anything. `CONFIG network` has a **Run port map test** button
beside the setting, and `PORTMAP TEST` does the same thing from the prompt.
All three protocols have a way of being asked that creates nothing, so the
test is a question and not a trial run.

It tells you three things: whether your router answers at all, which of the
three protocols it speaks, and what your outside address is. That last one is
the one to read first, because if it is a private address then nothing on
this page will ever work and the reason is your internet provider rather than
your router.
:::

### Switching it on

- On the board, open `CONFIG network` and set **Have router forward**
  (**Port map** at 40 columns) to `yes`. It is `no` on a new board.
- The board asks the router straight away, and again every hour.
- `PORTMAP` shows what came of it. `PORTMAP NOW` asks again, which is what
  to press after changing something in the router's own menu.

Nothing else changes. The board listens on the same port it always did, and
callers on your own network reach it the same way.

### How it asks

There are three protocols for this and the board tries them in order: PCP,
then NAT-PMP, then UPnP. They do the same job, and routers differ in which
one they answer.

- **UPnP** is the one most home routers have, and usually the one already
  switched on. Its full name here is UPnP IGD, and a router's menu calls it
  UPnP.
- **NAT-PMP** came from Apple and is what Apple's own routers used. Some
  others have it too, MikroTik among them.
- **PCP** is the newer standard meant to replace NAT-PMP. Fewer routers
  answer it. The board asks for it first because a router that does not have
  it says so in a way that points straight at NAT-PMP.

Where any of them works, what you end up with is exactly the forward you
would have made by hand: a caller reaches your router, and your router sends
them to the board. Nothing of ours sits in the middle, and nothing of ours
has to keep running for it to work.

### Mapped is not the same as reachable

`PORTMAP` says **mapped**, and it never says reachable, because those are two
different claims. The board can see that the router agreed. It cannot see
whether anything from the internet actually arrives, because that needs
somebody outside to try. Dial your own board from a phone on mobile data,
with the phone's Wi-Fi switched off, to find out.

### What it can leave behind

A forward made this way is normally a lease. The board asks for two hours and
renews it halfway through, so a board switched off for good has its forward
expire by itself within a couple of hours.

Some routers will not do leases. They answer that the only forward they can
make is one that never expires, and the board takes it, because the
alternative is no forward at all. `PORTMAP` then shows **Lease: none**.

> **A forward that never expires outlives the board.** Setting **Have router
> forward** back to `no` while the board is running gives it back. Unplugging
> the board does not, because nothing on the board runs once the power is
> gone. The forward stays in the router, pointing at an address the router
> may later hand to some other device. If you are retiring a board, switch
> the setting off first, or delete the forward in the router yourself.

A forward you made by hand has exactly the same property. This is not a new
kind of risk; it is one you would not have thought to go looking for.

<!-- The protections belong to the protocols that have them, and only two of the three do. Sources, checked 2026-10-06: RFC 6886 section 3.2.1 for the NAT-PMP quote, and RFC 6887 section 15.1 for PCP's equivalent ("MUST only accept normal ... PCP requests from a client on the same interface from which it would normally receive packets from that client, and it MUST silently ignore PCP requests arriving on any other interface"). UPnP IGD has no counterpart: the UPnP Device Architecture makes site-local scope a MAY, so whether an IGD answers on the WAN side is the manufacturer's choice. The two figures are Rapid7's "Security Flaws in Universal Plug and Play", January 2013 (hdm.io/writing/SecurityFlawsUPnP.pdf: 81 million addresses answered SSDP from the internet over the 2012 scan, about 17 million of those also exposed the SOAP service) and Akamai's UPnProxy, 2018 (about 65,000 routers carrying injected NAT entries). Do not write "the standards say so plainly" about all three again: that was the defect here, and on the page that calls UPnP "the one most home routers have" it told a reader a real risk did not exist. Transparency not fear mongering (Rob): the exposed case is a bad router rather than the normal one, and the page says which. -->
### What to know about the security of it

UPnP has a reputation, and some of it is earned. Two different questions get
run together when people repeat it, so they are worth taking apart.

**Can somebody on the internet open a port in your router this way?** For two
of the three protocols, no, and their specifications say so in those terms.
NAT-PMP's, RFC 6886, requires that a gateway "MUST NOT accept mapping
requests destined to the NAT gateway's external IP address or received on its
external network interface", and PCP's, RFC 6887, says a server "MUST
silently ignore PCP requests arriving on any other interface" than the one it
normally hears that client on.

**UPnP's specification carries no such requirement**, and UPnP is the one most
home routers have. Nothing in it obliges a router to listen on the inside
only, so whether yours does is its manufacturer's decision rather than the
standard's, and some of them got it wrong. When Rapid7 asked every address on
the internet in 2012, 81 million of them answered a UPnP question from
outside, and about 17 million of those also offered the part that makes
forwards. In 2018 Akamai found roughly 65,000 routers carrying forwards a
stranger had put there from the internet and was pushing traffic through.

That is a badly built or badly set up router rather than the usual one, and it
is nothing to do with the board, which asks from inside your network the way
every router expects. It is worth knowing because it is the one thing on this
page you cannot check from the board and cannot fix with a setting on it: it
is your router's firmware. Keep that up to date. If you want it shut for
certain, switching UPnP off in the router closes the whole thing, for the
board and for everything else on your network, and plenty of people run that
way on purpose.

**What you take on by switching this on** is on your own side of the router,
and it is the part people repeat least. There is no password and no prompt.
Any device on your network can ask the router for a forward and get one, and
the router does not tell you it happened. A laptop with something nasty on it,
or a cheap gadget that has not been updated since it was made, can open a port
to itself by exactly the same route the board uses. That is the design and
not a fault in any particular router: these protocols were written for a home
network where everything on it was assumed to be trusted.

So the setting ships switched off, and leaving it off and forwarding the port
by hand is a perfectly reasonable choice. Forwarding by hand costs you one
more evening and it is an evening you are in charge of.

### It will tell you when your ISP is in the way

The useful side effect: the router hands back its own outside address, and
`PORTMAP` shows it. If that address is a private one, your router is not on
the internet directly and no forward of any kind will ever work, by hand or
otherwise. That is [CGNAT or a double
NAT](/docs/forward#two-things-that-will-stop-it-working), the thing most
likely to waste your evening, and `PORTMAP` says **NOT on the internet** in
those words rather than letting a working mapping look like a reachable
board.

For somebody behind a carrier NAT that is the whole answer rather than a step
on the way: there was never a setting to find. Switching the setting on to
learn it costs nothing either, because a forward made on a router that is not
itself on the internet reaches nobody: that is the same fact that makes the
answer bad news. Set it back to `no` afterwards if you like.

<!-- Firmware 1.2.3's PORTMAP TEST. The paragraph above is the 1.2.2 route and stays true after 1.2.3; this adds the better one rather than replacing it. -->
::: from 1.2.3
From firmware 1.2.3 the test says the same thing without forwarding anything,
which is why it is worth running before you go near the router at all.
:::

If no router answers at all, the board cannot tell you this, because there is
no reply to read the address out of.

### If the router gives you a different number

A router that already has your port spoken for can give the board a different
outside number instead. The board publishes the number it actually got, so
[your listing](/docs/announce) shows what callers should dial. Anyone you
gave the old number to by hand needs the new one.
:::

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

<!-- Both halves answer the same question, "is my router on the internet", and the reader who lands here from the aside at the top is most often behind a carrier NAT. On 1.2.2 the route is to switch the setting on and read PORTMAP, which is safe to recommend for exactly the reason that makes the answer bad news: a forward made on a router that is not on the internet is reachable by nobody. On 1.2.3 the test answers it with no forward at all. Additive, so the 1.2.2 reader is never left pointing at a section that is not on their page, and the anchor into the test's own section is inside the 1.2.3 half where that section exists. -->
::: from 1.2.2
Both of these are a question about one number, your router's own outside
address, and finding it usually means logging into the router. From firmware
1.2.2 the board can read it off the router for you: switch [the setting
above](/docs/forward#or-let-the-board-ask-your-router) on, and `PORTMAP`
shows the outside address the router handed back and says whether it is on
the internet at all.

If it comes back **NOT on the internet**, you are behind one of the two above
and that is your answer: there was never a router setting to find, and you
have saved yourself the evening. Nothing of yours was exposed by asking,
because a forward on a router that is not on the internet reaches nobody, and
you can set the setting back to `no`.

<!-- Firmware 1.2.3's PORTMAP TEST, moved out of 1.2.2 on 2026-10-06. -->
::: from 1.2.3
From firmware 1.2.3 you can have the same number without making a forward at
all: `PORTMAP TEST`, or the **Run port map test** button on `CONFIG network`,
asks the router for its outside address and nothing else. [The test makes no
forward](/docs/forward#finding-out-without-switching-anything-on), so it is
safe to run before you have decided anything.
:::
:::

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
