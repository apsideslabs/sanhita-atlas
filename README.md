# Sanhita Atlas

A full-text reference to the **Bharatiya Nyaya Sanhita, 2023** — the code that replaced the Indian Penal Code
on 1 July 2024.

**Live:** https://apsideslabs.github.io/sanhita-atlas/

## What it is

Every one of the 358 sections of the Act, extracted from the Gazette notification of 25 December 2023, each on
its own page with the statutory text, its chapter, the section that follows it, and the IPC provision it replaced.

- **358 section pages** — the text of the provision, set for reading
- **20 chapter pages** — ranges, subject matter and the sections inside
- **Browse** — all sections in one filterable table
- **Search** — Fuse.js over the full text of every section, opened with `/`
- **IPC to BNS** — 35 correspondences with notes where the provision was rewritten

## Stack

Static HTML and CSS. No framework, no build runtime in the browser.

| Layer | Choice |
| --- | --- |
| Type | Source Serif 4 (statute), Instrument Sans (UI), JetBrains Mono (numbers) |
| Interactivity | [Alpine.js](https://alpinejs.dev) 3 |
| Search | [Fuse.js](https://fusejs.io) over a static JSON index |
| Hosting | GitHub Pages |

## Structure

```
index.html            overview
browse.html           all 358 sections, filterable
chapters.html         20 chapter cards
chapter/N.html        a chapter and its sections
section/N.html        a single section
mapping.html          IPC to BNS correspondence
changes.html          new offences and what moved
about.html            404.html
assets/               css, js, search index, favicon
tools/                generator (build.py, parse.py, src/)
```

## Rebuilding

```bash
# 1. extract the Act from the Gazette PDF
python3 tools/parse.py        # -> sections.json

# 2. generate the site
python3 tools/build.py        # -> dist/
```

`tools/parse.py` reads the 102-page Gazette PDF and splits it into 358 sections using the section numbering,
the chapter headings and the marginal notes.

## Licence

MIT for the code. The statutory text is published by the Government of India and is not claimed here.
Not legal advice.
