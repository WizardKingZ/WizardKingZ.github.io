# WizardKingZ.github.io

Johnew Zhang's personal site, built with Jekyll and hosted on GitHub Pages. The design follows the same house format as the Trident Macro Monitor and Johnew's Kitchen: a navy band, underline tabs, ruled section heads and one accent colour per pillar.

## Writing a post

Add a Markdown file to `_posts/` named `YYYY-MM-DD-slug.md`. The slug becomes the URL (`/slug/`).

```yaml
---
title: "Post title"
date: 2026-10-24 09:00
pillar: academic        # investing | academic | culture | sports
series: research        # a group within the pillar; see `pillars` in _config.yml
topic: asset pricing    # optional, shown after the series name
summary: "One line shown in lists and search results."
takeaway: "Optional one-line callout at the top of the post."
tags: ["finance", "python"]
---
```

Math works as before: `$$...$$` for inline and display equations (MathJax 3). Images go in `assets/images/<post>/` and are referenced as `/assets/images/<post>/image.png`.

A pillar's tab appears on its own once it has its first post, so Investing, Culture and Sports stay hidden until there is something in them. Set `hidden: true` to keep a post online but out of every list.

## Adding a standalone HTML page

Standalone pages (such as Johnew's Kitchen) are copied in as-is. A one-line script adds a thin strip at the top with a link back to the site.

```bash
python3 scripts/add_page.py ~/Downloads/page.html my-page \
    --title "Page title" --pillar investing \
    --eyebrow "Short headline" --blurb "One sentence for the card."
```

This writes `my-page/index.html` and lists the page in `_data/standalone.yml`, so it shows on the home page and in its pillar's tab. Run the same command again to replace the HTML with a newer copy.

### Trident Macro Monitor

A scheduled task refreshes this copy every Sunday evening, after the private weekly Monitor update has published. It reads the private artifact, runs the two commands below, checks the page, and pushes it. It never changes the private Monitor or its update. To do it by hand, copy in the new export, then pack its data so the page source isn't readable:

```bash
python3 scripts/add_page.py ~/Downloads/trident-macro-monitor.html macro-monitor
python3 scripts/protect_page.py macro-monitor/index.html
```

`protect_page.py` rounds the data, swaps internal file names for provider names, minifies the code, and gzips and encodes everything. It also drops the PDF library and adds the copyright line to the footer. The browser unpacks it on load. This stops casual copying but not a determined visitor. It needs `node`.

### Johnew's Kitchen

The Kitchen keeps its recipes in its own database on claude.ai, so the copy here reads a snapshot from `kitchen/data/recipes.json`, `kitchen/data/pantry.json` and `kitchen/photos/`. To refresh it, ask Claude to re-export the Kitchen to this folder.

## Previewing locally

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000. The `github-pages` gem pins the same Jekyll and plugin versions GitHub uses.

## Layout

| Path | What it is |
|---|---|
| `_config.yml` | Name, links, pillars and series |
| `_layouts/` | `default`, `home`, `section` (pillar pages), `post`, `page` |
| `_includes/` | Head, header (band and tabs), footer, post row |
| `assets/css/site.css` | All styles, with light and dark tokens at the top |
| `assets/js/` | Theme toggle and table of contents (`site.js`); return strip (`return-strip.js`) |
| `academic.html`, `investing.html`, `culture.html`, `sports.html` | Pillar pages |
| `kitchen/` | Johnew's Kitchen, with its data and photos |
