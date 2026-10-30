# Sanhita Atlas

An installable **PWA** reference to the **Bharatiya Nyaya Sanhita, 2023** — the code that replaced the
Indian Penal Code on 1 July 2024.

**Live:** https://apsideslabs.github.io/sanhita-atlas/

## The app

- **Situation check** — a deterministic rules engine: answer fixed factual questions, and 41 rules
  evaluate against your answers to show which sections apply, with the reason for each match
- **358 sections** — full text extracted from the Gazette notification of 25 December 2023
- **21 annotated** — explanation, worked example and leading case law
- **Offline** — the whole code is cached by a service worker after first load
- **Installable** — add to home screen; runs standalone with its own icon and splash
- **Saved sections** — bookmarks kept in local storage
- **Search** — full-text, over every section

## Stack

| Layer | Choice |
| --- | --- |
| Shell | Hand-written HTML/CSS, hash router, no framework |
| Search | [Fuse.js](https://fusejs.io) over a static JSON bundle |
| Offline | Service worker, cache-first with stale-while-revalidate for CDN |
| Type | Plus Jakarta Sans, Source Serif 4, JetBrains Mono |
| Hosting | GitHub Pages |

## Structure

```
index.html               app shell (app bar, rail, tab bar)
manifest.webmanifest     install metadata and icons
sw.js                    offline cache
assets/css/app.css       design system
assets/js/app.js         router, views, search, bookmarks
assets/data/sections.json  358 sections + annotations (456 KB)
assets/data/rules.json     the rules engine: 5 scenarios, 45 questions, 41 rules
assets/icons/            app icons
tools/                   generator
```

## Rebuilding

```bash
python3 tools/parse.py     # Gazette PDF  -> sections.json
python3 tools/build.py     # sections + annotations -> assets/data/sections.json
```

## Licence

MIT for the code. The statutory text is published by the Government of India and is not claimed here.
Not legal advice.
