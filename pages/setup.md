<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- The setup hub (guides, 2026-09-29, tty-ux's sysop guide spec, internal/tty-ux-sysop-guide-2026-09-29.md in the site's working tree). Five steps in /install's numbered style, then a card for each part of the board, then Going public. Everything that was on this page moved whole to a page of its own: first-login, config, backups, chat, forums, info, announce, ssh, and the files and sd settings to sdcard. Every old anchor still lands here: #first-become-the-sysop on step 3, the plugins' on their cards, and the CONFIG pages' on the "Every setting" list, each a link to the same id on /docs/config. -->
# Set up your BBS

::: applies
Firmware 1.2.0
:::

From a board in a box to callers on it, in five steps.

::: guidetop
::: guide
Flash it | Put the software on the board from [the web installer](https://unleashedbbs.com/install). About five minutes.
Join your Wi-Fi | The installer asks for your network once it has flashed. [The Wi-Fi step](https://unleashedbbs.com/install#step-wifi)
Call it and become the sysop | Sign up, then give `unleashed` from your own network. [Each screen](/docs/first-login) | #first-become-the-sysop
Choose your own sysop password | The staff form opens by itself. F1 saves. [Why it matters](https://unleashedbbs.com/install#the-sysop-password)
Open the board | CONFIG board: Stop taking calls, no. Until then, it's busy.
:::

::: art
setup-steps
:::

Already running? Every setting is on [the CONFIG page](/docs/config).
Building it yourself? [Build from source](https://unleashedbbs.com/build#for-developers-build-from-source).
:::

## Add to your board

### On every board

::: art
#sd
:::

<!-- One card a line: title | url | description | tag | #id | icon (sitekit's CARD_ICONS). Tags are one form, "<thing> required" or "Firmware x.y.z+" (Rob, 2026-09-29). -->
::: cards
Chat and mail | /docs/chat | The chat room, private messages and their limits. | | #chat | chat
Forums | /docs/forums | Topics, and who may read, start and reply. | SD card required | #forums | forums
Files and the SD card | /docs/sdcard | File areas, uploads, and the card's own jobs. | SD card required | #files | sdcard
Information pages | /docs/info | The sysop's pages: INFO, and /i0 to /i9 in chat. | | #info | info
:::

### Hardware you add

::: cards
Camera and photos | /docs/camera | SNAPSHOT from a built-in camera or a camera sat. | Camera required | | camera
Sats | https://unleashedbbs.com/satellites | A camera or a door on a small box of its own, over the air. | Firmware 1.2.0+ | | sat
Lights | /docs/lights | A drive light and a strip of pixels, for a board in a case. | | #lights | lights
Screens and skins | /docs/skins | Dress a board's screen up as another machine. | S3 board required | | screen
:::

### Keeping it running

::: cards
Backups | /docs/backups | The settings, accounts and screens in one zip. | | #backup | backup
The directory listing | /docs/announce | Put your board on the list, so callers can find it. | | #announce | listing
SSH | /docs/ssh | Encrypted calls, the SSH port and the board's keys. | S3 board required | | lock
:::

## Going public

::: gopublic
[Forward port 6400](/docs/forward) when you want callers from outside your
own network, and not before the sysop password is yours. [Call the
board](/docs/terminals) from anything with a telnet client first, and see it as
your callers will.
:::

## Every setting

::: art
#how-config-works
#board
#limits
#accounts
#staff
#wifi
#network
#the-plugin-pages
:::

Every page of `CONFIG`, field by field, is on [the CONFIG
page](/docs/config): [how CONFIG works](/docs/config#how-config-works),
[board](/docs/config#board), [limits](/docs/config#limits),
[accounts](/docs/config#accounts), [staff](/docs/config#staff),
[network](/docs/config#network) and [the plugin
pages](/docs/config#the-plugin-pages).
