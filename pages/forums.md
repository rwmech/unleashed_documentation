<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Moved whole from setup.md's "forums" (guides, 2026-09-29, tty-ux's sysop guide spec). -->
# Forums

The message boards, in topic areas. They need a card, and they are **off** as
shipped, so the topics can be set up first. The card is on [adding an SD
card](/docs/sdcard).

## Settings

Every plugin page starts with the same four fields, which [the plugin
pages](/docs/config#the-plugin-pages) explain. Read, Write and Admin are
`all`, `users` and `co1`. CONFIG offers four topics, each a button like a file
area:

| Field | What it does |
|---|---|
| **Key** | The topic's folder on the card, up to 12 characters. |
| **Name** | What callers see, up to 24 characters. |
| **About** | One line about it, up to 40 characters. |
| **Read** | Who sees the topic. Unset, the plugin's Read. |
| **Start** | Who may start a new subject. Unset, this topic's Reply. |
| **Reply** | Who may add to a subject already started. Unset, the plugin's Write. |
| **Moderate** | Who may moderate the topic, which includes removing posts. Unset, the plugin's Admin. |

Start and Reply are separate so that a topic can be news: Start `co1` and Reply
`users` means staff post, and anybody with an account may answer.

Back to [Set up your BBS](/docs/setup).
