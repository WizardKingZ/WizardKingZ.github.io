#!/usr/bin/env python3
"""Add (or refresh) a standalone HTML page on the site.

Copies an HTML file to <slug>/index.html, adds the "back to the site" strip,
and lists the page in _data/standalone.yml so it shows on the home page and in
its pillar's tab.

Usage:
  python3 scripts/add_page.py path/to/page.html kitchen \
      --title "Johnew's Kitchen" --pillar culture \
      --eyebrow "Recipes, cooked and kept" \
      --blurb "Every recipe I've cooked and kept, in one format."

Re-running with the same slug replaces the HTML and keeps the existing listing
unless you pass new values. Run it from the repository root.
"""
import argparse
import os
import re
import sys

PILLARS = {"investing": "Investing", "academic": "Academic", "culture": "Culture", "sports": "Sports"}
DATA = "_data/standalone.yml"
STRIP = ('<script src="/assets/js/return-strip.js" data-section="{section}" '
         'data-section-url="/{pillar}/" data-title="{title}" defer></script>')


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def read_entries():
    if not os.path.exists(DATA):
        return [], ""
    text = open(DATA, encoding="utf-8").read()
    header = "".join(l for l in text.splitlines(True) if l.startswith("#"))
    entries, cur = [], None
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        m = re.match(r"^(- )?\s*([a-z_]+):\s*(.*)$", line)
        if not m:
            continue
        if m.group(1):
            cur = {}
            entries.append(cur)
        val = m.group(3).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1].replace('\\"', '"')
        cur[m.group(2)] = val
    return entries, header


def write_entries(entries, header):
    keys = ["slug", "title", "pillar", "url", "eyebrow", "blurb", "image"]
    out = [header.rstrip("\n")] if header else []
    for e in entries:
        first = True
        for k in keys:
            if e.get(k):
                out.append(("- " if first else "  ") + f"{k}: {yaml_str(e[k])}")
                first = False
    open(DATA, "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("slug")
    ap.add_argument("--title")
    ap.add_argument("--pillar", choices=sorted(PILLARS))
    ap.add_argument("--eyebrow")
    ap.add_argument("--blurb")
    ap.add_argument("--image", help="site path to a card image, e.g. /kitchen/photos/x.jpg")
    a = ap.parse_args()

    if not os.path.exists("_config.yml"):
        sys.exit("Run this from the repository root.")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", a.slug):
        sys.exit("Slug must be lower-case letters, digits and dashes.")

    entries, header = read_entries()
    entry = next((e for e in entries if e.get("slug") == a.slug), None)
    if entry is None:
        if not (a.title and a.pillar):
            sys.exit("A new page needs --title and --pillar.")
        entry = {"slug": a.slug, "url": f"/{a.slug}/"}
        entries.append(entry)
    for k in ("title", "pillar", "eyebrow", "blurb", "image"):
        v = getattr(a, k)
        if v:
            entry[k] = v

    html = open(a.html, encoding="utf-8").read()
    html = re.sub(r'\s*<script src="/assets/js/return-strip\.js"[^>]*></script>', "", html)
    strip = STRIP.format(section=PILLARS[entry["pillar"]], pillar=entry["pillar"],
                         title=entry["title"].replace('"', "&quot;"))
    idx = html.lower().rfind("</body>")
    html = (html[:idx] + strip + "\n" + html[idx:]) if idx >= 0 else (html + "\n" + strip + "\n")
    if html.lstrip().startswith("---"):
        sys.exit("The HTML starts with '---'; Jekyll would treat it as front matter.")

    os.makedirs(a.slug, exist_ok=True)
    open(os.path.join(a.slug, "index.html"), "w", encoding="utf-8").write(html)
    write_entries(entries, header)
    print(f"Added /{a.slug}/ under {PILLARS[entry['pillar']]}.")


if __name__ == "__main__":
    main()
