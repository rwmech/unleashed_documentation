<!--
 ===========================================================================
  µnleashed BBS guides
 ===========================================================================

 File:         README.md
 Purpose:      What this repository is, how a guide is written, and where
               it is served.

 Copyright 2026 - Robert Mech
 License:      Creative Commons Attribution-ShareAlike 4.0 International
 SPDX-License-Identifier: CC-BY-SA-4.0
 ===========================================================================
-->

# µnleashed BBS guides

The guides for [µnleashed BBS](https://github.com/rwmech/unleashed_BBS):
joining a board, setting one up, letting people outside your home in, and
adding an SD card, lights, a camera or a skin. They are served at
[unleashedbbs.net/docs](https://unleashedbbs.net/docs) by the
[directory](https://github.com/rwmech/unleashed_directory), and anybody may
share and adapt them under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

| | |
|---|---|
| `pages/` | one guide a file, in the site's small Markdown dialect; the file name is the address (`pages/setup.md` is `/docs/setup`) |
| `pages/index.md` | the page at `/docs` |
| `shots/` | screens captured from the board itself, which `::: art` draws as `shot-<name>` |
| `shots/capture/` | the tools that captured them, from the firmware's host build |
| `check.py` | this repository's test |

## Writing a guide

The dialect is deliberately small, and a form it does not have renders as a
paragraph rather than failing, so check a new shape before relying on it.

- `#` once, for the title; `##` and `###` below it. Headings get ids from
  their words, so a section is linked as `/docs/setup#first-become-the-sysop`.
- `- ` bullets and `1. ` steps; a wrapped item indents its continuation two
  spaces. Pipe tables. Fenced code, and ```` ```nowrap ```` for a short
  command whose words must not break on a phone.
- `> ` is an amber warning box; a first line of `[!NOTE]` makes it calm, and
  `[!TIP]` makes it the loud invitation.
- `**bold**`, `*italics*`, `` `code` `` and `[links](/docs/setup)`.
- `[[sysop]]` explains a BBS word where a newcomer first meets it, from the
  glossary in the directory's `sitekit.py`. A term must be in it.
- `<!-- ... -->` is a note for whoever edits the page and never renders; it
  starts a line.
- `::: art` with a drawing's name on each line, then `:::`: the directory
  draws it. `::: cta` is a page's one primary action, `::: next` a section's
  next step. `::: from 1.1.0` ... `:::` renders only once that firmware is
  released, `::: until 1.1.0` only until then, and `::: from esp32-cam` once
  the installer offers that board.

Links: another guide is `/docs/<page>`; a page of the directory is written
relative (`/how`, `/badges`, `/directory`); a page of the project's site is
written in full (`https://unleashedbbs.com/install`). The words: no em dash,
and the name is µnleashed, with its micro sign, outside code.

Every guide opens with a comment carrying its licence line, the same five
lines as `pages/index.md`.

## Keeping guides current

A guide is kept current in the same change that makes it wrong: a firmware,
camsat or site change that alters what a guide says updates the guide in
that change, not later. Every guide opens, straight under its title, with
its **Applies to versions** line:

```
::: applies
Firmware 1.2.0
:::
```

It names the released versions the guide is true for (firmware, and camsat
or site where they matter), never one that is not out yet, and it moves
with the guide. At each release, every guide's line is checked. `check.py`
fails a page without one.

## Testing

```sh
python3 check.py
```

Every page: its licence line and one title, its comments and blocks closed,
only the blocks and drawings the directory draws, every link to something
that exists, every screen in `shots/`. With a checkout of
`unleashed_directory` beside this one it also renders every page with the
directory's own engine. The directory's `selftest.py` fetches every guide
over HTTP as well.

## How it is published

The directory's `deploy/update.sh` pulls this repository alongside its own,
when `/etc/unleashed-directory/docs` names the checkout, and installs
`pages/` and `shots/` beside the directory. A push to `main` is on the site
at the next update.

## Licence

The guides and everything else here are under the Creative Commons
Attribution-ShareAlike 4.0 International licence: share them and adapt
them, credit "µnleashed BBS guides, Robert Mech", and share what you make
from them under the same licence. The full text is in [LICENSE](LICENSE).

## How it was built

Parts of the guides were developed with the help of AI tools, including
Claude and ChatGPT. The design, the decisions and the copyright are Robert
Mech's.
