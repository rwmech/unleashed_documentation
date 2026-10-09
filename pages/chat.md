<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Moved whole from setup.md's "chat" (guides, 2026-09-29, tty-ux's sysop guide spec). -->
# Chat and mail

The chat room, and the messages callers leave each other. On as shipped, and
anybody may talk, guests included.

::: art
shot-chat-line
:::

## Settings

Every plugin page starts with the same four fields, which [the plugin
pages](/docs/config#the-plugin-pages) explain.

::: art
shot-config-chat
:::

- **room**: The room's name. Takes up to 19 characters; as shipped, `Main`.
- **rate**: How many lines a minute one caller may send, with a burst of 8.
  Only the caller who trips it is told. Takes 6 to 600; as shipped, `80`.
- **history**: How many lines the room remembers, shown to whoever joins. Takes
  8 to 2000; as shipped, `48`.
- **mail_slots**: How many messages the board holds at once, for everyone. 0
  switches messages off. Takes 0 to 64; as shipped, `32`.
- **mail_chars**: The longest a message may be. Takes 16 to 512 characters; as
  shipped, `512`.
- **mail_days**: How long an unread message waits before it expires. Takes 1 to
  365 days; as shipped, `14`.

The chat page shows the settings the board's settings file already carries, so
the labels are their own names. The file also sets the room's colours
(`color_node`, `color_text` and so on), each one a colour name: black, white,
red, cyan, purple, green, blue, yellow, orange, brown, ltred, darkgrey, grey,
ltgreen, ltblue or ltgrey.

Messages are not private: the board keeps them as plain text.

Back to [Set up your BBS](/docs/setup).
