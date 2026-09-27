#!/usr/bin/env python3
"""
===========================================================================
 µnleashed BBS guides: check.py
===========================================================================

File:         check.py
Purpose:      The guides' own test. Every page is read the way the
              directory will serve it at unleashedbbs.net/docs/<page>:

                - it carries its licence line, and one "# " title;
                - its comments and its ":::" blocks open and close;
                - it uses only the blocks and drawings the directory draws;
                - every link inside the guides names a guide that exists,
                  a page of the directory, or a page of the project's site;
                - every captured screen it names is in shots/;
                - no em dash, and the name is spelled with its micro sign.

              With a checkout of unleashed_directory beside this one (or
              SELFTEST_DIRECTORY naming one), it also renders every page with
              the directory's own engine and checks the glossary terms and
              the drawings resolve. The directory's selftest.py renders them
              over HTTP as well.

Usage:        python3 check.py

Copyright 2026 - Robert Mech
License:      Creative Commons Attribution-ShareAlike 4.0 International
SPDX-License-Identifier: CC-BY-SA-4.0
===========================================================================
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
SHOTS = os.path.join(HERE, "shots")
SKINS = os.path.join(HERE, "skins")
passed = failed = 0

# The blocks the directory renders on a guide (sitekit's own: art, cta,
# next and cards; and the release gates, from and until).
BLOCKS = ("art", "cta", "next", "cards", "hero", "skins")
GATE = re.compile(r"^::: (from|until) \S+( \d+\.\d+\.\d+)?\s*$")
# The drawings the directory registers for the guides (server.py, ART).
ART = ("firstcall", "setup-steps", "term-modern", "term-chromebook", "term-commodore",
       "term-atari", "term-apple-amiga", "term-others", "term-terminals", "term-bridge",
       "sd-wiring", "lights-drive", "lights-strip", "camera-snap", "skin-parts")
# Pages of the directory itself, which a guide may link relatively.
DIRECTORY = ("/", "/directory", "/badges", "/how", "/rules", "/data", "/feed.xml",
             "/api/boards.json", "/docs")
# Pages of the project's site, which a guide links absolutely.
SITE = ("", "install", "hardware", "build", "different", "whofor", "kids", "teachers",
        "roadmap", "donate", "upgrade", "connected", "satellites", "directory")


def check(label, ok):
    global passed, failed
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if ok:
        passed += 1
    else:
        failed += 1
    return ok


def pages():
    return sorted(f[:-3] for f in os.listdir(PAGES) if f.endswith(".md"))


def prose(text):
    """A page with its fenced code and its comments taken out: what a reader
    reads as prose, and where a title or a link means something."""
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def main():
    names = pages()
    texts = {n: open(os.path.join(PAGES, n + ".md"), encoding="utf-8").read() for n in names}
    shots = {f[:-5] for f in os.listdir(SHOTS) if f.endswith(".json")} if os.path.isdir(SHOTS) else set()

    print("Every page is a page")
    check("there are guides, and an index", len(names) >= 15 and "index" in names)
    bad = [n for n in names if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,39}", n)]
    check("every page name is one the directory serves" + (f"  <- {bad}" if bad else ""), not bad)
    bad = [n for n, t in texts.items() if "SPDX-License-Identifier: CC-BY-SA-4.0" not in t.split("-->")[0]]
    check("every page opens with its licence line" + (f"  <- {bad}" if bad else ""), not bad)
    bad = [n for n, t in texts.items() if len(re.findall(r"^# \S", prose(t), re.M)) != 1]
    check("every page has exactly one title" + (f"  <- {bad}" if bad else ""), not bad)

    print("Comments and blocks open and close")
    bad = []
    for n, t in texts.items():
        opened = closed = 0
        for line in t.splitlines():
            s = line.strip()
            if s.startswith("<!--"):
                opened += 1
            if "-->" in s:
                closed += 1
        if opened != closed:
            bad.append(n)
    check("every comment is closed" + (f"  <- {bad}" if bad else ""), not bad)
    bad, unknown = [], []
    for n, t in texts.items():
        depth, fence = 0, False
        for line in t.splitlines():
            if line.startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            s = line.rstrip()
            if s.startswith("::: "):
                name = s[4:].strip()
                if name in BLOCKS or GATE.match(s):
                    depth += 1
                else:
                    unknown.append(f"{n}: {s}")
            elif s == ":::":
                depth -= 1
                if depth < 0:
                    break
        if depth != 0 or fence:
            bad.append(n)
    check("every ::: block and every fence is closed" + (f"  <- {bad}" if bad else ""), not bad)
    check("and every block is one the directory draws"
          + (f"  <- {unknown[:3]}" if unknown else ""), not unknown)

    print("Drawings and screens")
    missing = []
    for n, t in texts.items():
        for m in re.finditer(r"^::: art\n(.*?)^:::", t, re.M | re.S):
            for want in (w.strip() for w in m.group(1).splitlines()):
                if not want or want.startswith("#"):
                    continue
                if want.startswith("shot-"):
                    if want[5:] not in shots:
                        missing.append(f"{n}: {want}")
                elif want not in ART:
                    missing.append(f"{n}: {want}")
    check("every drawing named is one the directory has, every screen is in shots/"
          + (f"  <- {missing[:3]}" if missing else ""), not missing)
    bad = []
    for s in sorted(shots):
        try:
            doc = json.load(open(os.path.join(SHOTS, s + ".json"), encoding="utf-8"))
            if not (doc.get("cols") and doc.get("rows") and doc.get("attrs")
                    and str(doc.get("source", "")).startswith("unleashed BBS ")):
                bad.append(s)
        except (OSError, ValueError):
            bad.append(s)
    check("every capture is whole and says where it came from" + (f"  <- {bad}" if bad else ""),
          shots and not bad)

    print("Links")
    broken = []
    for n, t in texts.items():
        for href in re.findall(r"\]\(([^)\s]+)\)", prose(t)):
            path = href.split("#")[0]
            if href.startswith("#") or href.startswith(("mailto:",)):
                continue
            if href.startswith("/docs/"):
                if path[len("/docs/"):] not in names:
                    broken.append(f"{n}: {href}")
            elif href.startswith("/skins/"):
                if not os.path.isfile(os.path.join(SKINS, path[len("/skins/"):])):
                    broken.append(f"{n}: {href}")
            elif href.startswith("/"):
                if path not in DIRECTORY:
                    broken.append(f"{n}: {href}")
            elif href.startswith("https://unleashedbbs.com"):
                page = path[len("https://unleashedbbs.com"):].strip("/")
                if page not in SITE:
                    broken.append(f"{n}: {href}")
            elif href.startswith("https://unleashedbbs.net"):
                rest = path[len("https://unleashedbbs.net"):] or "/"
                if rest.startswith("/docs/"):
                    if rest[len("/docs/"):] not in names:
                        broken.append(f"{n}: {href}")
                elif rest not in DIRECTORY:
                    broken.append(f"{n}: {href}")
            elif not href.startswith(("http://", "https://")):
                broken.append(f"{n}: {href}")
    check("every link names a guide, a directory page or a page of the site"
          + (f"  <- {broken[:4]}" if broken else ""), not broken)
    # SyncTERM's own site stopped answering in September 2026; its current
    # home is its SourceForge project. A link to the old one is a dead
    # "Get SyncTERM" button (Rob found it).
    dead = [n for n, t in texts.items()
            if re.search(r"syncterm\.(bbsdev\.)?net", t, re.I)]
    check("no link to SyncTERM's old, dead site" + (f"  <- {dead}" if dead else ""),
          not dead)

    print("Words")
    dash = [n for n, t in texts.items() if "—" in t]
    check("no em dash anywhere" + (f"  <- {dash}" if dash else ""), not dash)
    plain = []
    for n, t in texts.items():
        body = re.sub(r"```.*?```", "", t, flags=re.S)
        body = re.sub(r"`[^`]*`", "", body)
        body = re.sub(r"\]\([^)]*\)", "]", body)
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        if re.search(r"(?<![\w./@µ-])unleashed(?![\w.-])", body, re.I):
            plain.append(n)
    check("the name is spelled with its micro sign outside code"
          + (f"  <- {plain}" if plain else ""), not plain)

    # With the directory beside this checkout, render with its engine.
    directory = os.environ.get("SELFTEST_DIRECTORY", os.path.join(HERE, "..", "unleashed_directory"))
    if os.path.isfile(os.path.join(directory, "sitekit.py")):
        print("Rendered with the directory's engine")
        sys.path.insert(0, os.path.abspath(directory))
        os.environ["DIRECTORY_DOCS_DIR"] = HERE
        # The directory's server, for the blocks and drawings it registers
        # on top of the engine; importing it opens nothing and serves nothing.
        import server as sitekit                      # noqa: E402
        unknown = []
        for n, t in texts.items():
            for m in re.finditer(r"\[\[([^\[\]|]{1,40})\]\]", t):
                if sitekit.gloss_key(m.group(1)) is None:
                    unknown.append(f"{n}: {m.group(1)}")
        check("every [[term]] is in the glossary" + (f"  <- {unknown[:3]}" if unknown else ""),
              not unknown)
        leaks = []
        for n, t in texts.items():
            html_out = sitekit.md_render(t)
            if re.search(r"^:::|<p>::: ", html_out, re.M) or "[[" in html_out:
                leaks.append(n)
        check("and no page leaves dialect markup showing" + (f"  <- {leaks}" if leaks else ""),
              not leaks)
    else:
        print("Rendered with the directory's engine: skipped, no checkout of"
              " unleashed_directory beside this one")

    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
