<!--
Part of the µnleashed BBS guides (unleashed_documentation).
Copyright 2026 - Robert Mech
License: Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
-->
<!-- Moved whole from setup.md's "info" (guides, 2026-09-29, tty-ux's sysop guide spec). -->
# Information pages

The ten information pages, which callers read with `INFO` and from the chat room
with `/i`. On as shipped: anybody may read them, and only the sysop may write.

## Settings

Every plugin page starts with the same four fields, which [the plugin
pages](/docs/config#the-plugin-pages) explain. CONFIG has a button for each of
Page 0 to Page 9:

| Field | What it does |
|---|---|
| **Title** | The page's title in the list, up to 24 characters. |
| **Read** | Who sees it. Unset, the plugin's Read. |

The text itself is not written in CONFIG: `INFO 3 EDIT` at the prompt opens
page 3 in the board's message editor.

Back to [Set up your BBS](/docs/setup).
