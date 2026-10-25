#!/usr/bin/env python3
"""Make a data-heavy standalone page (the Macro Monitor) harder to lift.

Run it on the page after scripts/add_page.py has copied it in:

  python3 scripts/protect_page.py macro-monitor/index.html

What it does to the embedded `const DATA = {...}` and the app script after it:
  1. Trims the payload to what the charts draw: daily history to the last
     5 years, weekly to the last 20, matching the page's frequency toggle
     (monthly and longer are kept in full),
     values rounded to 4 significant figures, and internal file names in the
     source labels replaced by provider names.
  2. Minifies the app code, then gzips and base64-encodes data and code
     together, so neither is readable in the page source. The browser
     unpacks it on load (DecompressionStream, in all current browsers).
  3. Applies the public-site edits: no To-do tab, PDF download hidden and the
     jsPDF library dropped, no J.P. Morgan or Green Street data or charts, and
     a copyright line in the footer.
  4. Refuses to write if any licensed series or private path is left.

This deters casual copying. It cannot stop a determined visitor: any data a
browser can chart, the visitor's browser already has.
Needs node and npx (terser is fetched on first run).
"""
import base64
import datetime as dt
import gzip
import json
import math
import os
import re
import subprocess
import sys
import tempfile

DAILY_YEARS, WEEKLY_YEARS, SIG = 5, 20, 4
MARK = "<!-- protected-page -->"

# Licensed sources that are never published. Their series are removed, and so
# is every chart left with nothing to draw (with its note and guide).
# Match is on the series' source label.
EXCLUDE = {"J.P. Morgan": r"J\.P\. Morgan", "Green Street": r"Green Street"}


SLOT = "<!--app-slot-->"
# Local paths and private names that must never appear in the public copy.
FORBIDDEN = ["/sessions", "4. Data Sources", "5. Macro Studies", "PM Tool", "Project Trident", "/Users/"]


def site_edits(head, app, tail):
    """Public-site presentation: no To-do tab and no PDF download."""
    app = re.sub(r"\{id:'todo',\s*label:'[^']*'\},?\s*", "", app)
    m = re.search(r"const TODO\s*=\s*\[", app)
    if m:
        depth, j, q = 0, m.end() - 1, None
        while j < len(app):
            ch = app[j]
            if q:
                if ch == "\\":
                    j += 1
                elif ch == q:
                    q = None
            elif ch in "'\"`":
                q = ch
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        app = app[:m.start()] + "const TODO = []" + app[j + 1:]
    html = head + SLOT + tail
    html = re.sub(r'<section id="todo" class="tab"(?! hidden)', '<section id="todo" class="tab" hidden style="display:none!important"', html)
    if "#pdfbtn,#pdfdlg{display:none!important}" not in html:
        html = html.replace("</style>", "#pdfbtn,#pdfdlg{display:none!important}\n</style>", 1)
    return html, app


def exclude_licensed(data, app):
    S = data["series"]
    owner = {}
    for k, s in S.items():
        for name, pat in EXCLUDE.items():
            if re.search(pat, s.get("source") or ""):
                owner[k] = name
    for k in owner:
        del S[k]
        (data.get("meta", {}).get("last_dates") or {}).pop(k, None)

    def fix_s(m):
        keys = re.findall(r"'([^']+)'", m.group(1))
        gone = [k for k in keys if k in owner]
        if not gone:
            return m.group(0)
        left = [k for k in keys if k not in owner]
        if left:
            return "s:[" + ",".join(f"'{k}'" for k in left) + "]"
        who = " and ".join(sorted({owner[k] for k in gone}))
        return f"s:[], licensed:'{who}'"

    app = re.sub(r"\bs:\[((?:'[^']*'\s*,?\s*)*)\]", fix_s, app)
    # Range scoreboard rows: drop excluded pairs, then any group left empty.
    app = re.sub(r"\['(" + "|".join(map(re.escape, owner)) + r")','[^']*'\],?", "", app) if owner else app
    app = re.sub(r",\]\]", "]]", app)
    app = re.sub(r"\s*\['[^']*', \[\]\],?", "", app)
    # Remove every chart left with no published series, with its note and guide.
    app, titles = drop_charts(app)
    notes = data.get("commentary", {}).get("notes", {})
    for t in titles:
        for k in [k for k in notes if k == t or k.startswith(t + " | ")]:
            del notes[k]
        data.get("guide", {}).pop(t, None)
    app = app.replace(" (see the J.P. Morgan series below)", "")
    for g in data.get("guide", {}).values():
        for k, v in g.items():
            if isinstance(v, list):
                g[k] = [x.replace("; J.P. Morgan series continues it", "") if isinstance(x, str) else x for x in v]
    return app, len(owner), titles


def drop_charts(app):
    """Delete `{t:'...', ... licensed:'...' ...}` chart objects, matching braces outside strings."""
    out, titles, i = [], [], 0
    for m in re.finditer(r"\{t:'", app):
        if m.start() < i:
            continue
        depth, j, q = 0, m.start(), None
        while j < len(app):
            ch = app[j]
            if q:
                if ch == "\\":
                    j += 1
                elif ch == q:
                    q = None
            elif ch in "'\"`":
                q = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        obj = app[m.start():j + 1]
        if "licensed:'" in obj:
            end = j + 1
            while end < len(app) and app[end] in " \t":
                end += 1
            if end < len(app) and app[end] == ",":
                end += 1
            out.append(app[i:m.start()])
            titles.append(re.match(r"\{t:'((?:[^'\\]|\\.)*)'", obj).group(1))
            i = end
    out.append(app[i:])
    return "".join(out), titles


def rnd(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v == 0 or not math.isfinite(v):
        return v
    r = round(v, SIG - 1 - int(math.floor(math.log10(abs(v)))))
    return int(r) if float(r).is_integer() and abs(r) < 1e15 else r


def deep_round(o):
    if isinstance(o, dict):
        return {k: deep_round(v) for k, v in o.items()}
    if isinstance(o, list):
        return [deep_round(v) for v in o]
    return rnd(o)


def trim(block, years, built):
    cut = (built - dt.timedelta(days=round(365.25 * years))).isoformat()
    keep = [i for i, d in enumerate(block["dates"]) if str(d)[:10] >= cut]
    block["dates"] = [block["dates"][i] for i in keep]
    block["values"] = [block["values"][i] for i in keep]


def clean_sources(data, app):
    """Run the page's own srcNames() over each source label, so only provider names ship."""
    m = re.search(r"const SRC_RULES\s*=\s*\[", app)
    f = app.find("function srcNames(")
    if not m or f < 0:
        return 0
    start, depth, i = f, 0, app.index("{", f)
    for j in range(i, len(app)):
        depth += {"{": 1, "}": -1}.get(app[j], 0)
        if depth == 0:
            end = j + 1
            break
    rules_end = app.index("];", m.end()) + 2
    raw = sorted({s["source"] for s in data["series"].values() if s.get("source")})
    js = (app[m.start():rules_end] + "\n" + app[start:end] +
          "\nconst raw=" + json.dumps(raw) + ";process.stdout.write(JSON.stringify(raw.map(r=>[r,srcNames(r)])));")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as t:
        t.write(js)
    try:
        pairs = dict(json.loads(subprocess.run(["node", t.name], capture_output=True, text=True, check=True).stdout))
    finally:
        os.unlink(t.name)
    for s in data["series"].values():
        if s.get("source") in pairs:
            s["source"] = pairs[s["source"]]
    return len(pairs)


def minify(code):
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "app.js")
        open(src, "w", encoding="utf-8").write(code)
        out = subprocess.run(["npx", "--yes", "terser", src, "--compress", "--mangle", "--ecma", "2020"],
                             capture_output=True, text=True, check=True).stdout
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()
    if MARK in html:
        sys.exit("Already protected. Re-run add_page.py with the original HTML first.")

    # The app script is the one that starts with `const DATA=`.
    sm = next((m for m in re.finditer(r"<script>(.*?)</script>", html, re.S) if "const DATA=" in m.group(1)), None)
    if not sm:
        sys.exit("No `const DATA=` script found.")
    body = sm.group(1)
    i = body.index("const DATA=") + len("const DATA=")
    data, end = json.JSONDecoder().raw_decode(body, i)
    app = body[end:].lstrip(";\n ")
    before = len(json.dumps(data, separators=(",", ":")))

    html, app = site_edits(html[:sm.start()], app, html[sm.end():])
    sm = None  # positions changed; html is now head + tail around a placeholder
    app, n_lic, dropped = exclude_licensed(data, app)
    built = dt.date.fromisoformat(data["meta"]["built"][:10])
    for s in data["series"].values():
        nat = s.get("native") or {}
        if "D" in nat:
            trim(nat["D"], DAILY_YEARS, built)
        if "W" in nat:
            trim(nat["W"], WEEKLY_YEARS, built)
    n_src = clean_sources(data, app)
    data = deep_round(data)
    payload = json.dumps(data, separators=(",", ":"))

    code = "window.DATA=" + payload + ";\n" + minify(app)
    packed = base64.b64encode(gzip.compress(code.encode("utf-8"), 9)).decode("ascii")
    loader = (MARK + '<script id="pk" type="application/octet-stream">' + packed + "</script>\n<script>"
              "(async()=>{const b=Uint8Array.from(atob(document.getElementById('pk').textContent),c=>c.charCodeAt(0));"
              "const t=await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).text();"
              "const s=document.createElement('script');s.textContent=t;document.body.appendChild(s);"
              "document.getElementById('pk').remove();})();</script>")
    html = html.replace(SLOT, loader, 1)

    # Drop jsPDF: the PDF download is disabled on the site.
    html = re.sub(r"<script>\s*/\*\* @license\s*\*\s*\* jsPDF.*?</script>", "", html, count=1, flags=re.S)

    # Copyright and reuse line in the page's own footer.
    notice = (f"<span>&copy; {built.year} Johnew Zhang. Charts are for viewing only; "
              "the data may not be copied or redistributed.</span>")
    html, n = re.subn(r'(<div class="ft-top">.*?)(</div>)', lambda m: m.group(1) + notice + m.group(2),
                      html, count=1, flags=re.S)
    if not n:
        html = html.replace("</body>", f'<p style="text-align:center;font-size:12px;opacity:.7">{notice}</p></body>', 1)

    # Self-check before writing: nothing licensed or private may ship.
    bad = [k for k in data["series"] if re.match(r"(jpm|gs)_", k)]
    bad += [s for s in FORBIDDEN if s in code or s in html]
    if bad:
        sys.exit("Refusing to write; found: " + ", ".join(bad[:10]))

    open(path, "w", encoding="utf-8").write(html)
    print(f"Data {before/1e6:.1f} MB -> {len(payload)/1e6:.1f} MB; {n_lic} licensed series and {len(dropped)} charts removed; {n_src} source labels cleaned; "
          f"page now {len(html)/1e6:.1f} MB.")


if __name__ == "__main__":
    main()
